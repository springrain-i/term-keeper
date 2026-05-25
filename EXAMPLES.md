# Examples

## Add a Term

User:

```text
Use term-keeper.
以后 Fulfillment Window 指订单承诺时间到实际签收时间之间的时间差，记到词典里。
```

Expected behavior:

- The agent reads the current dictionary.
- The agent presents a confirmation table.
- The agent writes Markdown and HTML only after approval.

## Correct a Boundary

User:

```text
Agent Router 不是调度器，它只负责识别请求类型并转交给对应 agent。
```

Expected behavior:

- Classify as an agent or role boundary.
- Ask for confirmation.
- Preserve the anti-example: it is not a scheduler.

## Deprecate a Meaning

User:

```text
废弃 Old Score 这个口径，以后统一叫 Quality Score。
```

Expected behavior:

- Keep the deprecated meaning visible.
- Add or update the active term.
- Update both Markdown and HTML.

## Frequency-Only Update

User:

```text
Fulfillment Window 这个词在这次 PRD 里继续沿用。
```

Expected behavior:

- If the term already exists, increment trigger frequency by 1.
- Do not ask for a definition confirmation table.
- Do not routinely report the increment unless the user asks.

## Should Not Write

User:

```text
今天 Agent Router 跑失败了，先记一下。
```

Expected behavior:

- Do not update the dictionary.
- Treat it as transient runtime state, not durable semantics.
