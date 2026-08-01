# Decision Log — 字段顺序测试

**Date**: 2026-07-03
**Topic**: 测试解析器鲁棒性
**Depth**: light
**Status**: complete

---

## Decisions

### D1: 字段顺序测试 Alpha

**Answer**: 我们选择选项 A，因为它更简单。
**Status**: [RESOLVED]
**Downstream impact**: D2（下一个决策）
**Trade-off accepted**: 以灵活性换取更快交付
**Question**: 我们应该选择哪个选项？

---

### D2: 字段顺序测试 Beta

**Status**: [RISKY]
**Question**: 我们如何处理失败？
**Answer**: 使用指数退避重试。
**Downstream impact**: None（叶子节点）

---

### D3: 缺少可选字段

**Status**: [DEFERRED]
**Question**: 未来扩展怎么办？
**Answer**: 我们将在 Q3 处理。

---
