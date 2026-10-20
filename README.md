# Resolving Unknown Water Service Materials in Cornwall: A Comparison of Verification Strategies

独立研究工作区 · 初始搭建日期：2026-10-19（America/New_York）

在有限工时或预算下，居民自查、公共管段档案核查与现场检查应如何组合，才能让更多完整服务管线获得可靠分类？

**当前阶段：研究前基础搭建。** 这不是已完成的研究，也不是供水部门已确认的数据产品。

从 [START_HERE.md](START_HERE.md) 进入。研究范围见 [research/brief.md](research/brief.md)，下一步见 [research/TASKS.md](research/TASKS.md)，agent 分工见 [agents/README.md](agents/README.md)。

## 快速开始

```sh
uv sync --locked
make check
make fetch
make preflight
```

`make fetch` 访问公开原始来源并保存本地快照；`make preflight` 生成搭建期诊断。原始文件和行级衍生数据不提交 Git。克隆仓库后需重新抓取本地原始数据。Python 3.11+；依赖记录在 `uv.lock`。

## 目录

- `.codex/agents/`：项目范围的真实 Codex custom-agent 配置，继承用户模型和权限。
- `research/`：研究范围、分析计划、证据／来源清单、任务和决策。
- `data/seed/`、`data/schema/`、`data/manifests/`：可版本控制的种子表、结构和抓取收据。
- `data/raw/`、`data/interim/`、`data/processed/`、`data/restricted/`：只在本地保留的原始或行级数据。
- `src/`、`scripts/`、`tests/`：可复现方法与关键研究口径检查。
- `reports/`：可以审阅的汇总结果；不含逐户地址或坐标。

研究拟服务 Cornwall-on-Hudson Water Department；尚未取得部门台账或联系部门。AI 协助搭建和分析须在将来对外成果中披露。无自动监控、无人值守研究或后台模型任务。
