# Agent roles and handoffs

This workspace uses the official [project-scoped custom-agent format](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents). Each `.codex/agents/*.toml` file defines `name`, `description` and `developer_instructions`. Model settings, permissions and tools inherit from the parent session. At most three child agents may run concurrently.

| Agent | Responsibility |
|---|---|
| `research_lead` | Research coordination and scope control |
| `data_steward` | Inventory cleaning, duplicate review and provenance |
| `strategy_modeler` | Verification resource allocation and scenario comparison |
| `workflow_researcher` | Local verification workflows and research context |
| `methods_reviewer` | Independent methodology, boundary and disclosure review |

The lead defines the task; source and data roles prepare inputs; the analyst produces reproducible outputs; an independent reviewer performs a read-only review; the lead integrates and verifies the result. Configuring agents does not start them automatically. All responses, documents and handoffs must use English.

Every handoff must include `task_id`, input paths and snapshot hashes, output paths, evidence and assumptions, verification commands and results, unresolved items and the next responsible role. Assign exclusive write paths. Reviewers must not edit the artifacts they review.

`AGENTS.md` also supports this workflow in a single-agent session. If the client cannot dispatch a custom agent, read the corresponding TOML as a role specification and execute the phases sequentially. State clearly that no independent child agent ran.
