"""Deterministic workflow contract; no fitted rates, optimizer or acceptance policy."""
from dataclasses import dataclass, replace
from inventory_audit import material_state

ACTIONS = {
    'public_records': ('public',),
    'resident_assisted': ('customer',),
    'field_public': ('public',),
    'field_customer': ('customer',),
    'joint_field_visit': ('public', 'customer'),
}
OUTCOMES = {'evidence_returned', 'no_response', 'inconclusive', 'access_failed', 'cancelled'}


@dataclass(frozen=True)
class Side:
    reported_material: str = 'Unknown'
    evidence_status: str = 'unreviewed'
    evidence_ref: str | None = None

    def __post_init__(self):
        if self.evidence_status not in {'unreviewed', 'submitted', 'accepted', 'rejected'}:
            raise ValueError('Unknown evidence status')
        if self.evidence_status == 'accepted' and (
            material_state(self.reported_material) != 'reported_known' or not self.evidence_ref):
            raise ValueError('Accepted side evidence requires a known label and evidence reference')


@dataclass(frozen=True)
class Case:
    public: Side = Side()
    customer: Side = Side()
    attempts: int = 0
    staff_minutes: float = 0
    accepted_category: str | None = None
    acceptance_rule_ref: str | None = None
    acceptance_decision_ref: str | None = None


def fully_evidenced_pair(case):
    return case.public.evidence_status == case.customer.evidence_status == 'accepted'


def eligible(case, action):
    if action not in ACTIONS:
        raise ValueError('Unknown action')
    return case.accepted_category is None and any(
        getattr(case, side).evidence_status != 'accepted' for side in ACTIONS[action])


def apply_attempt(case, action, outcome, *, effort_minutes, updates=None):
    """Evidence statuses are supplied by review, never inferred from method names."""
    if not eligible(case, action):
        raise ValueError('Action has no unresolved evidence target, or case is already accepted')
    if outcome not in OUTCOMES or effort_minutes is None or effort_minutes < 0:
        raise ValueError('Explicit outcome and nonnegative observed/scenario effort required')
    updates = updates or {}
    if outcome != 'evidence_returned' and updates:
        raise ValueError('Failed/inconclusive contact cannot silently resolve evidence')
    for side, evidence in updates.items():
        if side not in ACTIONS[action] or not isinstance(evidence, Side):
            raise ValueError('Evidence must apply to a side targeted by this action')
        if getattr(case, side).evidence_status == 'accepted':
            raise ValueError('Reopening accepted evidence requires a separate reviewed correction')
    return replace(case, **updates, attempts=case.attempts + 1,
                   staff_minutes=case.staff_minutes + effort_minutes)


def record_department_decision(case, category, *, rules_confirmed, rule_ref, decision_ref,
                               effort_minutes):
    """Record an externally established decision; do not derive regulatory rules.

    Some accepted categories may not require both material labels to be known.
    The referenced department/state rule must determine sufficiency, outside this
    contract. Two accepted side labels alone never create an accepted category.
    """
    if not rules_confirmed or not rule_ref or not decision_ref:
        raise ValueError('Confirmed acceptance rules and a documented decision are required')
    if effort_minutes is None or effort_minutes < 0:
        raise ValueError('Classification review effort must be recorded')
    if category not in {'Lead', 'Non-Lead', 'GSLRR'}:
        raise ValueError('Resolved category must be supplied explicitly')
    return replace(case, accepted_category=category, acceptance_rule_ref=rule_ref,
                   acceptance_decision_ref=decision_ref, attempts=case.attempts + 1,
                   staff_minutes=case.staff_minutes + effort_minutes)
