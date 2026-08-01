#!/usr/bin/env python3
"""
grill-me 决策树可视化工具

将 decision-log.md 转换为可视决策树图。
支持 Mermaid、ASCII 艺术和 DOT（Graphviz）输出格式。

用法：
    python decision_tree_visualizer.py decision-log.md --format mermaid
    python decision_tree_visualizer.py decision-log.md --format ascii
    python decision_tree_visualizer.py decision-log.md --format dot > tree.dot
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_decision_log(content: str) -> list[dict]:
    """解析 decision-log.md 并提取决策及其关系。

    使用一个不依赖字段顺序或分隔符风格的稳健解析器。
    通过 ### D{n}: 标题找到所有决策章节，然后提取每个章节内
    直到下一个决策标题或主要章节边界之前的字段。
    """
    decisions = []

    # 查找所有决策标题：### D1: 标题
    header_pattern = re.compile(r'^### (D\d+):\s*(.+?)$', re.MULTILINE)
    headers = list(header_pattern.finditer(content))

    for i, header in enumerate(headers):
        decision_id = header.group(1)
        title = header.group(2).strip()

        # 确定块内容：从当前标题末尾到下一个标题开头
        start = header.end()
        if i + 1 < len(headers):
            end = headers[i + 1].start()
        else:
            end = len(content)
        block = content[start:end]

        # 从块中提取所有 **字段**: 值 对
        # 匹配 **字段名**: 值（值持续到下一个 **字段 或块末尾）
        fields = {}
        field_pattern = re.compile(r'\*\*(.+?)\*\*:\s*(.+?)(?=\n\*\*|$)', re.DOTALL)
        for fm in field_pattern.finditer(block):
            field_name = fm.group(1).strip().lower().replace(' ', '_')
            field_value = fm.group(2).strip()
            fields[field_name] = field_value

        # 将 'none' 下游影响归一化为空
        downstream = fields.get('downstream_impact', '')
        if downstream.lower().startswith('none'):
            downstream = ''

        decisions.append({
            'id': decision_id,
            'title': title,
            'status': fields.get('status', '[OPEN]'),
            'question': fields.get('question', ''),
            'answer': fields.get('answer', ''),
            'tradeoff': fields.get('trade-off_accepted', ''),
            'downstream': downstream,
        })

    return decisions


def build_tree(decisions: list[dict]) -> tuple[dict[str, list[str]], set[str]]:
    """根据下游影响字段构建父子关系。
    
    解析 downstream impact 字段以找到显式的决策引用。
    "D2（描述）, D3（描述）" 表示当前决策是 D2 和 D3 的父决策。
    
    返回：
        tree: 父 ID 到子 ID 列表的映射
        roots: 没有父决策的根决策 ID 集合
    """
    id_set = {d["id"] for d in decisions}
    
    # parents[child] = 父决策列表
    parents: dict[str, list[str]] = {d["id"]: [] for d in decisions}
    
    for d in decisions:
        downstream = d.get("downstream", "")
        if not downstream:
            continue
        # 按逗号/分号拆分并提取每个部分开头的决策 ID
        parts = re.split(r'[,;]', downstream)
        for part in parts:
            part = part.strip()
            # 匹配每个部分开头的决策 ID
            match = re.match(r'^(D\d+)\b', part)
            if match:
                other_id = match.group(1)
                if other_id in id_set and other_id != d["id"]:
                    if d["id"] not in parents[other_id]:
                        parents[other_id].append(d["id"])
    
    # 转换为 tree（父 -> 子）
    tree: dict[str, list[str]] = {d["id"]: [] for d in decisions}
    for child_id, parent_ids in parents.items():
        for parent_id in parent_ids:
            if child_id not in tree[parent_id]:
                tree[parent_id].append(child_id)
    
    # 对子决策排序以保持输出一致
    for parent_id in tree:
        tree[parent_id].sort()
    
    # 根决策是没有父决策的决策
    roots = {d["id"] for d in decisions if not parents[d["id"]]}
    
    return tree, roots


def status_icon(status: str) -> str:
    """返回决策状态的可视化指示符。"""
    if "RESOLVED" in status:
        return "[OK]"
    elif "RISKY" in status:
        return "[!]"
    elif "DEFERRED" in status:
        return "[>>]"
    return "[?]"


def status_emoji(status: str) -> str:
    """返回适用于所有输出格式的 ASCII 安全状态指示符。

    使用纯 ASCII，避免在 Windows GBK 终端上出现 UnicodeEncodeError。
    Mermaid/DOT/ASCII 格式都使用此函数以保持一致和可移植。
    """
    return status_icon(status)


def to_mermaid(decisions: list[dict], tree: dict[str, list[str]], roots: set[str]) -> str:
    """生成 Mermaid 流程图。"""
    lines = ["```mermaid", "flowchart TD"]
    
    # 添加节点
    for d in decisions:
        icon = status_emoji(d["status"])
        safe_title = d["title"].replace('"', '\\"')
        lines.append(f'    {d["id"]}["{icon} {d["id"]}: {safe_title}"]')
    
    # 添加边
    for parent_id in sorted(tree.keys()):
        for child_id in tree[parent_id]:
            lines.append(f"    {parent_id} --> {child_id}")
    
    # 添加样式类
    lines.append("")
    lines.append("    classDef resolved fill:#90EE90,stroke:#228B22")
    lines.append("    classDef risky fill:#FFD700,stroke:#FF8C00")
    lines.append("    classDef deferred fill:#87CEEB,stroke:#4169E1")
    lines.append("    classDef open fill:#FFB6C1,stroke:#DC143C")
    
    for d in decisions:
        if "RESOLVED" in d["status"]:
            lines.append(f"    class {d['id']} resolved")
        elif "RISKY" in d["status"]:
            lines.append(f"    class {d['id']} risky")
        elif "DEFERRED" in d["status"]:
            lines.append(f"    class {d['id']} deferred")
        else:
            lines.append(f"    class {d['id']} open")
    
    lines.append("```")
    return "\n".join(lines)


def to_ascii(decisions: list[dict], tree: dict[str, list[str]], roots: set[str]) -> str:
    """生成 ASCII 艺术树。"""
    lines = ["决策树", "=" * 50, ""]
    
    decision_map = {d["id"]: d for d in decisions}
    
    def render_node(node_id: str, prefix: str = "", is_last: bool = True) -> list[str]:
        result = []
        d = decision_map[node_id]
        icon = status_icon(d["status"])
        connector = "└── " if is_last else "├── "
        result.append(f"{prefix}{connector}{icon} {d['id']}: {d['title']}")
        
        children = tree.get(node_id, [])
        new_prefix = prefix + ("    " if is_last else "|   ")
        
        for i, child_id in enumerate(children):
            result.extend(render_node(child_id, new_prefix, i == len(children) - 1))
        
        return result
    
    for root_id in sorted(roots):
        lines.extend(render_node(root_id, "", True))
        lines.append("")
    
    lines.append("图例：[OK]=已解决 [!]=有风险 [>>]=已推迟 [?]=开放")
    return "\n".join(lines)


def to_dot(decisions: list[dict], tree: dict[str, list[str]], roots: set[str]) -> str:
    """生成 Graphviz DOT 格式。"""
    lines = [
        "digraph DecisionTree {",
        '    rankdir="TB";',
        '    node [shape=box, style="rounded,filled", fontname="Helvetica"];',
        '    edge [fontname="Helvetica"];',
        ""
    ]
    
    status_colors = {
        "RESOLVED": "#90EE90",
        "RISKY": "#FFD700",
        "DEFERRED": "#87CEEB",
        "OPEN": "#FFB6C1",
    }
    
    for d in decisions:
        color = "#D3D3D3"
        for status_key, color_val in status_colors.items():
            if status_key in d["status"]:
                color = color_val
                break
        safe_title = d["title"].replace('"', '\\"')
        label = f"{status_emoji(d['status'])} {d['id']}:\\n{safe_title}"
        lines.append(f'    {d["id"]} [label="{label}", fillcolor="{color}"];')
    
    for parent_id in sorted(tree.keys()):
        for child_id in tree[parent_id]:
            lines.append(f"    {parent_id} -> {child_id};")
    
    lines.append("}")
    return "\n".join(lines)


def _set_utf8_stdout() -> None:
    """强制将 stdout 设为 UTF-8 编码，防止在 Windows GBK
    终端和其他非 UTF-8 环境中出现 UnicodeEncodeError。"""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        # 针对 StringIO 或其他非文件 stdout 对象的回退
        pass


def main() -> int:
    _set_utf8_stdout()

    parser = argparse.ArgumentParser(
        description="将 grill-me 决策日志可视化为决策树"
    )
    parser.add_argument("input_file", type=Path, help="decision-log.md 的路径")
    parser.add_argument(
        "--format",
        choices=["mermaid", "ascii", "dot"],
        default="mermaid",
        help="输出格式（默认：mermaid）",
    )
    parser.add_argument("-o", "--output", type=Path, help="输出文件（默认：stdout）")
    args = parser.parse_args()
    
    if not args.input_file.exists():
        print(f"错误：找不到文件：{args.input_file}", file=sys.stderr)
        return 1
    
    content = args.input_file.read_text(encoding="utf-8")
    decisions = parse_decision_log(content)
    
    if not decisions:
        print("警告：日志文件中未找到任何决策。", file=sys.stderr)
        return 1
    
    tree, roots = build_tree(decisions)
    
    if args.format == "mermaid":
        output = to_mermaid(decisions, tree, roots)
    elif args.format == "ascii":
        output = to_ascii(decisions, tree, roots)
    elif args.format == "dot":
        output = to_dot(decisions, tree, roots)
    else:
        output = to_mermaid(decisions, tree, roots)
    
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"输出已写入 {args.output}")
    else:
        print(output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
