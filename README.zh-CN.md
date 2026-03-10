# eric-awesome-skills

**个人技术工具箱** — 一个为 [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) 设计的 Skills 合集，收录各种提升效率的实用小工具。

每个 Skill 都是独立、可对话触发的工作流，自动完成复杂的多步任务。Skills 遵循开放的 [SKILL.md 标准](https://docs.openclaw.ai/tools/clawhub)，兼容 Claude Code、Codex CLI、Gemini CLI 和 OpenClaw。

[English](README.md) | [中文](README.zh-CN.md)

---

## 📦 Skills 列表

| Skill | 简介 | 触发词 | 备注 | Preview |
|-------|------|--------|------|------| 
| [karpathy-curated-rss-brief](skills/karpathy-curated-rss-brief/) | 从 Karpathy 精选的 93 个 RSS 源抓取最近文章，生成高质量中文日报 | `RSS 日报`、`karpathy-curated-rss-brief` | 灵感来源：[Karpathy 的 RSS 列表](https://x.com/karpathy/status/2018043254986703167) 和 [Cory Doctorow 谈 RSS](https://pluralistic.net/2026/03/07/reader-mode/)。Skill 页面：[YouMind](https://youmind.com/~skills/019c4fce-220b-7f35-974b-0cc543b7682d)。[查看完整灵感来源 →](skills/karpathy-curated-rss-brief/README.md#灵感来源) | <img src="assets/KarpathyRssBeginning.png" width="480" alt="日报开头"> <img src="assets/KarpathyRssEnding.png" width="480" alt="日报结尾"> |
---

## 🚀 安装

### 方式一 — ClawHub（推荐）

通过 [ClawHub](https://clawhub.ai) 注册中心一键安装：

```bash
# 安装 ClawHub CLI
npm install -g clawhub

# 安装 Skill
clawhub install karpathy-curated-rss-brief
```

### 方式二 — skills.sh（npx）

```bash
npx skills add https://github.com/MESevenJourney/eric-awesome-skills.git --skill karpathy-curated-rss-brief
```

### 方式三 — Claude Code 插件市场

将本仓库添加到 Claude Code 插件市场，再浏览安装对应的 skill：

```
/plugin marketplace add MESevenJourney/eric-awesome-skills
```

然后打开插件浏览器，找到并安装：

```
/plugin
```

找到 `karpathy-curated-rss-brief`，选择 **Install**。

### 依赖

部分 Skills 使用 Python 脚本，需要安装 [`uv`](https://docs.astral.sh/uv/)：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

脚本通过 [PEP 723](https://peps.python.org/pep-0723/) inline metadata 自动管理依赖，无需手动 `pip install`。

---

## 📖 使用示例

安装完成后，在 Claude Code 对话中直接输入触发词：

```
RSS 日报
```

Claude 会自动执行完整工作流：抓取 RSS 订阅源 → 筛选文章 → 读取全文 → 生成中文日报并保存到本地。



---

## 📜 开源协议

[MIT License](LICENSE) — 自由使用、修改和分发。
