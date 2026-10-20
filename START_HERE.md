# 开始之前

1. 读 `AGENTS.md`、`research/brief.md` 和 `research/STATUS.md`。
2. 运行 `uv sync --locked && make check`；本地原始数据不存在时先 `make fetch`。
3. 读 `reports/preflight.md`，区分本次快照复现的数字、用户预研和未完成核验。
4. 从 `research/TASKS.md` 第一个未完成任务开始，每项任务先明确输入、文件归属、输出和验收。

**建议首条研究指令：**

> 请开始 L01：确认 locality 与供水系统边界、字段含义和重复记录规则，再建立可审计的基线。先阅读本项目 AGENTS.md、研究范围和已有 preflight；把证据、推断与待核对事项分开。需要团队时先给每个角色明确产物和互不冲突的文件归属，再按 agents/README.md 调用相应 agent。暂不联系部门或居民。

正式研究尚未启动。配置了 agent 不代表 agent 已执行或其结果已被独立审查。`methods_reviewer` 的独立审查在有真实分析产物后进行。
