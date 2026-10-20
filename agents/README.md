# Agent 分工与交接

配置采用 OpenAI 官方 [project-scoped custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)：每个 `.codex/agents/*.toml` 定义 name、description、developer_instructions。模型、权限与工具继承父会话；最多同时启动 3 个子 agent。

| Agent | 任务 |
|---|---|
| `research_lead` | 研究协调与范围控制 |
| `data_steward` | 台账清洗、去重与证据来源 |
| `strategy_modeler` | 核查资源配置与情景比较 |
| `workflow_researcher` | 本地核验流程与研究定位 |
| `methods_reviewer` | 独立方法、边界与披露审查 |

常规顺序：lead 明确任务 → 来源／数据角色完成输入 → 分析角色产生可复现产物 → reviewer 独立只读审查 → lead 整合并核验。未发出研究指令时不自动运行。

每次交接必须包含：`task_id`、输入路径及快照／SHA、输出路径、证据／假设、验证命令与结果、未解决事项、下一责任角色。并行写入同一文件禁止；reviewer 不改被审查文件。

`AGENTS.md` 保证普通单 agent 会话也能完成相同流程。若当前客户端不能识别 custom agent，则读对应 TOML 作为角色说明顺序执行，并明确说明没有独立 agent 执行。
