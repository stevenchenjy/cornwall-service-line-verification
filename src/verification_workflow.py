"""Deterministic evidence/review contract; no fitted rates or regulatory policy.

Pinned local documents and attributed validation records establish the intake
boundary. File hashes check integrity, not the authenticity of an authority.
"""
from dataclasses import dataclass, replace, asdict
from datetime import date
from pathlib import Path
import hashlib
import json
import math
from inventory_audit import material_state, normalized

ACTIONS = {
    'public_records': ('public',), 'resident_assisted': ('customer',),
    'field_public': ('public',), 'field_customer': ('customer',),
    'joint_field_visit': ('public', 'customer'),
    'evidence_review': ('public', 'customer'), 'classification_review': (),
}
OUTCOMES = {'evidence_returned', 'no_response', 'inconclusive', 'access_failed', 'cancelled'}
REVIEW_OUTCOMES = {'classification_accepted', 'classification_rejected', 'classification_deferred'}


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
class ReviewEvent:
    action: str
    outcome: str
    effort_minutes: float
    previous_category: str | None
    category_after: str | None
    decision_id: str | None = None
    decision_record_sha256: str | None = None
    decision_record_path: str | None = None
    supersedes_decision_id: str | None = None
    correction_reason: str | None = None
    validation_error: str | None = None
    public_before: Side = Side()
    customer_before: Side = Side()
    public_after: Side = Side()
    customer_after: Side = Side()


@dataclass(frozen=True)
class Case:
    public: Side = Side()
    customer: Side = Side()
    case_id: str = ''
    pws_id: str = ''
    baseline_as_of: str = ''
    attempts: int = 0
    staff_minutes: float = 0
    accepted_category: str | None = None
    acceptance_rule_ref: str | None = None
    acceptance_decision_ref: str | None = None
    review_history: tuple[ReviewEvent, ...] = ()


def fully_evidenced_pair(case):
    return case.public.evidence_status == case.customer.evidence_status == 'accepted'


def state_fingerprint(case):
    state={key:getattr(case,key) for key in ('case_id','pws_id','baseline_as_of','accepted_category','acceptance_decision_ref')}
    state.update(public=asdict(case.public),customer=asdict(case.customer))
    return hashlib.sha256(json.dumps(state,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def _effort(value):
    if value is None or not math.isfinite(value) or value < 0:
        raise ValueError('Explicit finite nonnegative staff effort is required; missing is not zero')


def eligible(case, action):
    if action not in ACTIONS:
        raise ValueError('Unknown action')
    if case.accepted_category is not None:
        return False
    if action == 'classification_review':
        return True  # A review can defer or reject even when material is unresolved.
    if action == 'evidence_review':
        return any(getattr(case,s).evidence_status == 'submitted' for s in ('public','customer'))
    return any(getattr(case,s).evidence_status != 'accepted' for s in ACTIONS[action])


def apply_attempt(case, action, outcome, *, effort_minutes, updates=None):
    if action == 'classification_review':
        raise ValueError('Use classification_review() so decision validation and review history are preserved')
    if not eligible(case, action):
        raise ValueError('No unresolved target, or case already accepted; correction requires the separate path')
    _effort(effort_minutes)
    if outcome not in OUTCOMES:
        raise ValueError('Unknown attempt outcome')
    updates=updates or {}
    if outcome != 'evidence_returned' and updates:
        raise ValueError('Failed/inconclusive contact cannot resolve evidence')
    for side,evidence in updates.items():
        if side not in ACTIONS[action] or not isinstance(evidence,Side):
            raise ValueError('Evidence must apply to a targeted side')
        if getattr(case,side).evidence_status == 'accepted':
            raise ValueError('Accepted evidence requires an explicit correction path')
        if action == 'resident_assisted' and evidence.evidence_status != 'submitted':
            raise ValueError('Resident submissions must be assessed in a separate evidence-review event')
        if action == 'evidence_review' and (getattr(case,side).evidence_status != 'submitted'
                or evidence.evidence_status not in {'accepted','rejected'}):
            raise ValueError('Evidence review assesses a submitted item as accepted or rejected')
    return replace(case,**updates,attempts=case.attempts+1,staff_minutes=case.staff_minutes+effort_minutes)


def _read_pinned(root, pointer):
    root=Path(root).resolve()
    if not isinstance(pointer,dict) or not pointer.get('path') or not pointer.get('sha256'):
        raise ValueError('A document path and SHA256 are required')
    relative=Path(pointer['path'])
    path=(root/relative).resolve()
    if relative.is_absolute() or not path.is_relative_to(root):
        raise ValueError('Evidence path must remain inside the restricted evidence root')
    data=path.read_bytes()
    if not data or hashlib.sha256(data).hexdigest() != pointer['sha256']:
        raise ValueError('Referenced evidence is empty or its SHA256 does not match')
    return data


def _reviewed_document(record,root):
    if not isinstance(record,dict):
        raise ValueError('A structured document record is required')
    validation=record.get('validation',{})
    if not isinstance(validation,dict) or validation.get('status') != 'validated' or not validation.get('reviewer_id'):
        raise ValueError('Documented, attributed validation is required')
    date.fromisoformat(validation.get('reviewed_on',''))
    _read_pinned(root,record.get('source'))


def _validated_decision(case,root,pointer,*,correction):
    if root is None or pointer is None:
        raise ValueError('No validated decision bundle supplied; final acceptance remains pending')
    record=json.loads(_read_pinned(root,pointer))
    _reviewed_document(record,root)
    if not case.case_id or not case.pws_id or not case.baseline_as_of:
        raise ValueError('A dated stable-ID system-specific case is required')
    date.fromisoformat(case.baseline_as_of)
    if any(record.get(key) != getattr(case,key) for key in ('case_id','pws_id','baseline_as_of')):
        raise ValueError('Decision does not match case, system or baseline date')
    if record.get('state_fingerprint') != state_fingerprint(case):
        raise ValueError('Decision is stale or does not match the evidence state')
    if record.get('outcome') != 'classification_accepted' or not record.get('decision_id'):
        raise ValueError('A validated accepted decision record is required')
    date.fromisoformat(record.get('decided_on',''))
    if correction:
        if (record.get('supersedes_decision_id') != case.acceptance_decision_ref
                or record['decision_id'] == case.acceptance_decision_ref or not record.get('correction_reason')):
            raise ValueError('Correction must identify the superseded decision and reason')
    elif record.get('supersedes_decision_id'):
        raise ValueError('Correction record cannot be used for an initial acceptance')
    rule=json.loads(_read_pinned(root,record.get('rule')))
    _reviewed_document(rule,root)
    if (not rule.get('rule_id') or rule.get('pws_id') != case.pws_id
            or rule.get('category') != record.get('category')
            or record['category'] not in {'Lead','Non-Lead','GSLRR'}):
        raise ValueError('Rule/category/system mismatch')
    # Each alternative is a department-reviewed category-specific evidence pattern.
    # At least one supported side is required; no universal two-side rule is invented.
    satisfied=False
    for alternative in rule.get('evidence_alternatives',[]):
        if not isinstance(alternative,dict) or not alternative or not set(alternative) <= {'public','customer'}:
            continue
        if not all(isinstance(m,list) and m and all(isinstance(v,str) for v in m) for m in alternative.values()):
            continue
        if all(getattr(case,side).evidence_status == 'accepted'
               and normalized(getattr(case,side).reported_material) in {normalized(m) for m in materials}
               for side,materials in alternative.items()):
            for side in alternative:
                _read_pinned(root,record.get('evidence',{}).get(getattr(case,side).evidence_ref))
            satisfied=True
            break
    if not satisfied:
        raise ValueError('Accepted side evidence does not satisfy the reviewed category-specific rule')
    return record,rule


def _review(case,outcome,effort_minutes,root,pointer,*,correction=False,updates=None):
    _effort(effort_minutes)
    if outcome not in REVIEW_OUTCOMES:
        raise ValueError('Review must accept, reject or defer')
    if correction != (case.accepted_category is not None):
        raise ValueError('Accepted categories require the separate correction procedure')
    target=replace(case,**(updates or {}))
    record=rule=None
    error=None
    if outcome == 'classification_accepted':
        try:
            record,rule=_validated_decision(target,root,pointer,correction=correction)
        except (ValueError,TypeError,KeyError,OSError,json.JSONDecodeError) as exc:
            # Failed validation preserves effort and a visible deferred review.
            error=str(exc);outcome='classification_deferred'
    accepted=record is not None
    new_category=record['category'] if accepted else case.accepted_category
    event=ReviewEvent(action='classification_correction' if correction else 'classification_review',
        outcome=outcome,effort_minutes=effort_minutes,previous_category=case.accepted_category,
        category_after=new_category,decision_id=record['decision_id'] if accepted else None,
        decision_record_sha256=pointer['sha256'] if accepted else None,
        decision_record_path=pointer.get('path') if isinstance(pointer,dict) else None,
        supersedes_decision_id=record.get('supersedes_decision_id') if accepted else None,
        correction_reason=record.get('correction_reason') if accepted else None,
        validation_error=error,public_before=case.public,customer_before=case.customer,
        public_after=target.public if accepted else case.public,
        customer_after=target.customer if accepted else case.customer)
    return replace(target if accepted else case,accepted_category=new_category,
        acceptance_rule_ref=rule['rule_id'] if accepted else case.acceptance_rule_ref,
        acceptance_decision_ref=record['decision_id'] if accepted else case.acceptance_decision_ref,
        attempts=case.attempts+1,staff_minutes=case.staff_minutes+effort_minutes,
        review_history=case.review_history+(event,))


def classification_review(case,outcome,*,effort_minutes,evidence_root=None,decision_record=None):
    return _review(case,outcome,effort_minutes,evidence_root,decision_record)


def record_department_decision(case,*,effort_minutes,evidence_root=None,decision_record=None):
    """Compatibility entry point; category/boolean/string-only acceptance removed."""
    return classification_review(case,'classification_accepted',effort_minutes=effort_minutes,
                                 evidence_root=evidence_root,decision_record=decision_record)


def correct_department_decision(case,*,effort_minutes,evidence_root=None,decision_record=None,
                                corrected_sides=None,outcome='classification_accepted'):
    updates=corrected_sides or {}
    if not set(updates) <= {'public','customer'} or not all(isinstance(v,Side) for v in updates.values()):
        raise ValueError('Corrections can update only documented side evidence')
    return _review(case,outcome,effort_minutes,evidence_root,decision_record,
                   correction=True,updates=updates)
