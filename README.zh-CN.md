# Term Keeper

**Agent 词典管家**，一个用于维护项目术语表 / 概念词典的可复用 Codex Skill。

[English README](README.md) · [Agent 阅读版](README.agent.md)

你是否遇到过这些问题：

- Agent 压缩上下文后，忘记了关键定义。
- Agent 对某些词的理解，和你的真实口径有偏差。
- 同一个模块名、指标名、角色边界，在不同对话里被反复解释错。
- 临时运行状态被误写成长期项目概念。

`term-keeper` 的作用，就是给项目建立一层稳定的“词义记忆”：Markdown 给 Agent 读，HTML 表格给人审阅，所有定义类写入都必须先经过用户确认。

## 效果预览

![Term Keeper HTML 词表截图](screenshots/demo-glossary-table.png)

![Term Keeper 确认流程图](screenshots/confirmation-table-flow.png)

## 它解决什么

- 把长期概念从聊天上下文里沉淀到项目文件。
- 防止 Agent 把推断当成用户定义。
- 保留业务词、角色边界、废弃口径和展示语义。
- 同时维护 Agent 可读的 Markdown 和用户可审阅的 HTML 表格。
- 不绑定某个具体项目路径，可以复用到不同开放项目。

## 工作方式

1. 用户明确提出定义、修正、改名、废弃或边界说明。
2. Agent 先整理成确认表。
3. 用户确认或修正表格内容。
4. Agent 再同步维护 `docs/glossary.md` 和 `docs/glossary.html`。
5. Python 脚本只是可选辅助，用于生成、检查、CI 或发布前校验；日常维护由 Agent 直接完成。

## 适合记录什么

- 业务术语和领域概念。
- 模块名称及其含义。
- Agent、角色、岗位或流程边界。
- 驾驶舱、报表、指标展示口径。
- 流水线状态、交接语义、产物定义。
- 已废弃或已改名的旧口径。

## 仓库结构

真正可安装的 skill 包在：

```text
skill/term-keeper/
  SKILL.md
  agents/openai.yaml
  examples/demo-glossary.html
  references/dictionary-config-template.md
  references/pressure-test-scenarios.md
  scripts/render_glossary_html.py
  scripts/check_dictionary_sync.py
```

仓库根目录的 README、截图、License、测试说明是给 GitHub 用户看的，不属于 skill 本体。

## 快速开始

把 `skill/term-keeper/` 复制到你的 Codex skills 目录，然后对 Codex 说：

```text
Use term-keeper.
以后 "Agent Router" 指识别请求类型并转交给对应 Agent 的组件。它不是调度器。
```

Agent 应该先输出确认表。只有你确认后，才会写入词典。

## 默认输出文件

如果项目里还没有自己的词典配置，默认使用：

```text
docs/glossary.md
docs/glossary.html
```

Markdown 是 Agent 友好的维护入口；HTML 是表格审阅版，方便使用者检查词条。

## 可选脚本

- `skill/term-keeper/scripts/render_glossary_html.py`：把默认 Markdown 结构渲染成 HTML 表格。
- `skill/term-keeper/scripts/check_dictionary_sync.py`：检查 Markdown 和 HTML 是否同步。

脚本不是强依赖。Agent 可以直接维护 Markdown 和 HTML；脚本更适合发布前校验、CI 或批量生成。

## Demo

GitHub Pages 展示页：

```text
https://springrain-i.github.io/term-keeper/
```

启用 GitHub Pages 后即可访问。设置方式：仓库 `Settings -> Pages -> Build and deployment -> main / docs`。

本地 HTML demo：

```text
skill/term-keeper/examples/demo-glossary.html
```

截图已放在上方“效果预览”部分，GitHub 打开中文版 README 就能直接看到。

## 更多

- [INSTALLATION.md](INSTALLATION.md)：安装说明。
- [EXAMPLES.md](EXAMPLES.md)：使用示例。
- [TESTING.md](TESTING.md)：最小校验方式。
- [README.agent.md](README.agent.md)：给 Agent 读取的精简版。
