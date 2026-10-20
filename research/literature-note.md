# Initial literature and workflow check

This is a targeted first pass, not a systematic review or an originality finding. Sources were inspected October 19, 2026 (America/New_York); saved public-source receipts are in data/manifests/retrievals.csv.

| Source and inspection | Relevance / limit |
|---|---|
| [Sohail, 2026 preprint](https://arxiv.org/html/2608.19922v1), data/design/limitations reviewed | Compares recorded classifications across populations rather than paired prediction/excavation results. Warns about locality units, repeated records and shifted metadata descriptions. It does not estimate Cornwall action success rates. |
| [Selected code at e82c208](https://github.com/msarmadsohail/predictive-lead-service-line-audit/tree/e82c208baa431601c8c7cc81e1d3df61c8a30071), README, nyc_core.py and extract.py read | The NYC loader normalizes locality/address and truncates ZIP before retaining the first duplicate key. Cornwall retains repeated rows and ZIP extensions pending a policy. The source's analysis was not rerun; its choices are not adopted as local identity rules. |
| [Smart et al., Water Research 246:120725, 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC11107698/), abstract and study design read; DOI 10.1016/j.watres.2023.120725 | A Bennington control-home study compares stepwise identification combinations and costs. It supports examining sequences and evidence quality. Its selected known-material controls and setting do not supply Cornwall contact/acceptance probabilities or attempt denominators. |
| [Abernethy et al., ActiveRemediation, 2018](https://arxiv.org/abs/1806.10692), abstract checked; DOI 10.1145/3219819.3219896 | Describes inspection/replacement choices adapting to incoming Flint information. Full-method review remains pending; a different decision target and setting limit direct transfer. |

The [official local page](https://cornwall-on-hudson.gov/Departments/Water/Lead-Service-Lines) offers resident self-inspection/submission or a departmental visit. It does not document the full internal workflow, acceptance rules, attempt outcomes or effort. No local baseline process is inferred beyond these public options.

The [official NYS guidance PDF](https://www.health.ny.gov/environmental/water/drinking/docs/service_line_inventory_guidance_lcrr.pdf) returned HTTP 403 in this session, including a second ordinary retrieval attempt. Its operative acceptance requirements have not been inspected here. Obtain the current applicable department/state rules rather than treating a preprint's discussion as authority.

**October 20 source-check follow-up:** the preceding access result is historical. A browser-user-agent retry successfully retrieved the main official PDF, identical to the alternate official-host bytes. The retrieved document is August 2025 v3. Its relevant pages and the August 2024 dataset dictionary/overview have now been text/visually inspected by the current AI session; see the [official-source review](../reports/official-guidance-review.md), [page-level evidence](official-source-evidence.csv) and pinned receipt manifest. This resolves document access, not current local rule applicability, empirical calibration or independent human verification.

Next literature work should appraise full adaptive/stepwise methods, selection/attempt denominators and local contractor reports after the baseline and decision are confirmed. No claim that this local workflow analysis is novel has been established.
