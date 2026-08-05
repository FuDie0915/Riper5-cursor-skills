# Decision Log — 支付网关集成

**Date**: 2026-07-03
**Topic**: 为电商平台设计支付流程
**Depth**: medium
**Status**: complete

---

## Decisions

### D1: 支付服务商选择

**Status**: [RESOLVED]
**Question**: 初期上线应该使用哪个支付服务商？
**Answer**: 卡支付使用 Stripe，PayPal 作为兜底
**Trade-off accepted**: 更高的单笔交易手续费（2.9% + 30¢），换取更快的集成速度和更好的开发者体验
**Local evidence**: 未找到现有支付代码
**External evidence**: Stripe 是初创公司的事实标准；PayPal 覆盖不愿输入卡号的用户
**Terms defined**: PaymentIntent（Stripe 的统一支付对象）、Webhook endpoint
**Downstream impact**: D2（webhook 处理）、D3（幂等策略）

---

### D2: Webhook 处理策略

**Status**: [RESOLVED]
**Question**: 如何异步处理 Stripe webhook 的支付事件？
**Answer**: 将 webhook 入队到 Redis，异步处理并带重试逻辑
**Trade-off accepted**: 引入 Redis 依赖和复杂度；避免阻塞 webhook 响应并应对流量峰值
**Local evidence**: 不存在 webhook 基础设施
**External evidence**: Stripe 建议在 5 秒内响应；排队是标准做法（Shopify、GitHub）
**Terms defined**: Webhook endpoint 签名验证、idempotency key
**Downstream impact**: D3（依赖 D1 的 PaymentIntent 流程）

---

### D3: 幂等与重复扣款防护

**Status**: [RISKY]
**Question**: 如果用户点了两次“支付”，如何防止重复扣款？
**Answer**: 在 PaymentIntent 创建时使用 Stripe 的幂等键，加上订单级别的去重
**Trade-off accepted**: 订单状态机复杂度增加；网络分区存在潜在边界情况
**Local evidence**: 订单状态机存在，但无幂等逻辑
**External evidence**: Stripe 文档推荐幂等键；支付行业标准（PCI 合规）
**Terms defined**: Idempotency key、network partition、exactly-once processing
**Downstream impact**: None（叶子决策）

---

### D4: 退款流程设计

**Status**: [DEFERRED]
**Question**: 退款应该由用户自助发起还是仅管理员可操作？
**Answer**: MVP 阶段仅管理员；自助退款在 v2 考虑
**Trade-off accepted**: 初期支持负担更高；推迟复杂的授权和欺诈防护
**Local evidence**: 管理后台存在，但无退款 UI
**External evidence**: 多数电商起步时仅管理员；自助退款需要滥用防护
**Terms defined**: Refund window（30 天）、partial refund
**Downstream impact**: None（推迟到 v2）

---

## Risk Register

| ID | Risk | Severity | Mitigation | Owner |
|----|------|----------|------------|-------|
| R1 | 高负载下重复扣款 | high | 幂等键 + 监控 | 后端团队 |
| R2 | Webhook 投递失败 | medium | 重试队列 + 死信队列 | 后端团队 |
| R3 | 退款滥用（v2） | medium | 限流 + 审计日志 | 产品团队 |

---

## Terminology Updates

| Term | Definition | Alias/avoid |
|------|------------|-------------|
| PaymentIntent | Stripe 的统一支付对象，代表一次支付尝试 | _Avoid_: charge, transaction |
| Idempotency key | 确保重复请求产生相同结果的唯一键 | _Avoid_: dedup key |
| Webhook endpoint | 接收 Stripe 异步事件通知的 HTTPS URL | _Avoid_: callback URL |

---

## ADRs Created

- `docs/adr/0001-stripe-over-paypal.md` — 选择 Stripe 作为主要支付服务商

---

## Open Questions (Deferred)

- 自助退款政策 — 推迟到 v2（触发条件：月退款请求量 > 100）
- 多币种支持 — 推迟到国际扩张上线

---

## Handoff Notes

Recommended next step: `to-prd`
Key context for implementer: D3 标记为 [RISKY] — 确保幂等实现在上线前有充分的测试覆盖
