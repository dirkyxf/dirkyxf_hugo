---
title: "Tailscale SSH 的 check 模式：为什么又要重新验证？"
description: "解释 Tailscale SSH check 模式的重新认证周期，以及减少验证次数和改用 accept 的区别。"
slug: tailscale-ssh-check-mode
date: 2026-11-02T19:38:46+08:00
tags:
  - Tailscale
  - SSH
draft: false
---

如果 Tailscale SSH 连接前再次要求验证，而匹配到的 SSH 规则使用了 `"action": "check"`，通常是 check 模式在要求重新认证。默认周期是 12 小时；实际周期由匹配的规则决定。Tailscale 会优先采用更严格的 check 规则，所以只新增一条 accept 规则未必能覆盖已有的 check 规则。

想减少验证次数、但仍保留周期性检查，可以在现有匹配规则中设置 `"checkPeriod": "168h"`，也就是最长 7 天。官方允许的范围是 1 分钟至 168 小时；`720h`（30 天）不受支持，而且自定义周期仅适用于 Premium 和 Enterprise 计划。不要用整段新策略覆盖原有配置，只改对应规则。

如果确实不需要这条规则额外要求重新验证，可以把它的 `action` 从 `check` 改为 `accept`。这只影响该规则涵盖的来源、目标和系统用户；网络访问策略仍须允许连接，用户也仍须通过 tailnet 身份认证。修改前先检查所有会匹配该连接的 SSH 规则。

设置位置在 Tailscale 管理控制台的 Access controls 页面，查看策略文件中的 `ssh` 规则。具体选哪种，取决于你是想少弹几次验证，还是完全取消这条规则的额外确认。

参考：[Tailscale SSH 文档](https://tailscale.com/docs/features/tailscale-ssh) · [策略文件语法](https://tailscale.com/docs/reference/syntax/policy-file)
