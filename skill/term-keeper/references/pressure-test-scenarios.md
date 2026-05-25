# Pressure Test Scenarios

Use these scenarios to test whether the skill behaves correctly in new projects.

## Should Update

- User: "以后 Fulfillment Window 指订单承诺到实际签收之间的时间差，记到词典里。"
- Expected: Present a confirmation table first. Add or update Markdown plus HTML only after the user approves.

- User: "Agent Router 不是调度器，它只负责把请求分类并转交给对应 agent。"
- Expected: Present a confirmation table first. Mark the impact as agent/role boundary and write Markdown plus HTML only after approval.

- User: "废弃 Old Score 这个口径，以后统一叫 Quality Score。"
- Expected: Present a confirmation table first. After approval, mark old term deprecated and add/update the active term in Markdown plus HTML.

## Should Not Update

- User: "今天 Agent Router 跑失败了，先记一下。"
- Expected: Do not write dictionary; this is run state.

- User: "我觉得 Fulfillment Window 可能可以理解成履约周期，你怎么看？"
- Expected: Do not write as user-confirmed definition; answer or ask for confirmation.

## Frequency Only

- User: "Fulfillment Window 这个词在这次 PRD 里继续沿用。"
- Expected: If the term already exists, increment trigger frequency by 1 in Markdown and HTML without changing the definition.

- Agent use: The agent uses "Agent Router" to route or validate a workflow request.
- Expected: If the term already exists and the use is intentional, increment trigger frequency by 1 in Markdown and HTML without scanning history.

## Should Ask First

- User: "以后 Dashboard 的异常数直接用客服工单数。"
- Expected: Present a confirmation table and explicitly call out reporting/data-source impact before updating.

- User: "PRD Agent 后面也负责测试验收。"
- Expected: Present a confirmation table and explicitly call out agent responsibility impact before updating.

## Verification Expectations

- New projects create and maintain both `docs/glossary.md` and `docs/glossary.html`.
- Projects that explicitly disable HTML pass with `check_dictionary_sync.py --md docs/glossary.md`.
- Markdown plus HTML projects pass with both `--md` and `--html`.
- Runtime/status language produces warnings unless it is clearly part of a durable boundary.
