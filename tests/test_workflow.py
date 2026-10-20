"""Synthetic local evidence bundles test the contract, not actual acceptance rules."""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from verification_workflow import (Case,Side,eligible,apply_attempt,fully_evidenced_pair,
    record_department_decision,classification_review,correct_department_decision,state_fingerprint)


class WorkflowChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.case=Case(case_id='synthetic-case',pws_id='synthetic-system',baseline_as_of='2026-10-20')

    def artifact(self,name,body):
        data=json.dumps(body,sort_keys=True).encode() if isinstance(body,dict) else body.encode()
        (self.root/name).write_bytes(data)
        return dict(path=name,sha256=hashlib.sha256(data).hexdigest())

    def decision(self,case,category='Non-Lead',*,decision_id='synthetic-decision',correction=False):
        source=self.artifact('source-'+decision_id+'.txt','Synthetic source document; no real department decision.')
        validation=dict(status='validated',reviewer_id='synthetic-reviewer',reviewed_on='2026-10-20')
        alternatives=[{'public':['Copper'],'customer':['Copper']}] if category=='Non-Lead' else [{'public':['Lead']}]
        rule=self.artifact('rule-'+decision_id+'.json',dict(rule_id='synthetic-rule-'+category,
            pws_id=case.pws_id,category=category,evidence_alternatives=alternatives,
            source=source,validation=validation))
        evidence={s.evidence_ref:self.artifact('evidence-'+str(i)+'.txt','Synthetic evidence '+str(i))
                  for i,s in enumerate([case.public,case.customer]) if s.evidence_ref}
        body=dict(decision_id=decision_id,case_id=case.case_id,pws_id=case.pws_id,
            baseline_as_of=case.baseline_as_of,state_fingerprint=state_fingerprint(case),
            outcome='classification_accepted',category=category,decided_on='2026-10-20',
            source=source,validation=validation,rule=rule,evidence=evidence)
        if correction: body.update(supersedes_decision_id=case.acceptance_decision_ref,correction_reason='Synthetic corrected source evidence')
        return self.artifact('decision-'+decision_id+'.json',body)

    def complete_case(self):
        return replace(self.case,public=Side('Copper','accepted','synthetic-public'),customer=Side('Copper','accepted','synthetic-customer'))

    def accept(self,case=None):
        case=case or self.complete_case()
        return record_department_decision(case,effort_minutes=2,evidence_root=self.root,decision_record=self.decision(case))

    def test_both_unknown_records_resident_then_separate_review(self):
        case=apply_attempt(self.case,'public_records','evidence_returned',effort_minutes=10,
            updates={'public':Side('Copper','accepted','synthetic-public')})
        case=apply_attempt(case,'resident_assisted','evidence_returned',effort_minutes=12,
            updates={'customer':Side('Copper','submitted','synthetic-customer')})
        self.assertFalse(fully_evidenced_pair(case));self.assertTrue(eligible(case,'evidence_review'))
        case=apply_attempt(case,'evidence_review','evidence_returned',effort_minutes=3,
            updates={'customer':Side('Copper','accepted','synthetic-customer')})
        self.assertTrue(fully_evidenced_pair(case));self.assertIsNone(case.accepted_category)
        case=self.accept(case)
        self.assertEqual((case.attempts,case.staff_minutes),(4,27))
        self.assertEqual(case.accepted_category,'Non-Lead')
        self.assertFalse(eligible(case,'classification_review'))

    def test_materials_without_accepted_evidence_remain_eligible(self):
        case=replace(self.case,public=Side('Copper'),customer=Side('Copper'))
        self.assertTrue(eligible(case,'public_records'));self.assertTrue(eligible(case,'resident_assisted'))
        self.assertFalse(fully_evidenced_pair(case))

    def test_no_response_submission_rejection_and_retry_effort(self):
        case=apply_attempt(self.case,'resident_assisted','no_response',effort_minutes=5)
        case=apply_attempt(case,'resident_assisted','evidence_returned',effort_minutes=8,
            updates={'customer':Side('Copper','submitted','synthetic-blurry-photo')})
        case=apply_attempt(case,'evidence_review','evidence_returned',effort_minutes=2,
            updates={'customer':Side('Copper','rejected','synthetic-blurry-photo')})
        self.assertTrue(eligible(case,'resident_assisted'))
        self.assertEqual((case.attempts,case.staff_minutes),(3,15));self.assertIsNone(case.accepted_category)

    def test_actions_cannot_rewrite_other_side_or_accept_resident_submission(self):
        with self.assertRaises(ValueError): apply_attempt(self.case,'resident_assisted','evidence_returned',effort_minutes=5,updates={'public':Side('Copper','accepted','x')})
        with self.assertRaises(ValueError): apply_attempt(self.case,'resident_assisted','evidence_returned',effort_minutes=5,updates={'customer':Side('Copper','accepted','x')})
        with self.assertRaises(ValueError): apply_attempt(self.case,'public_records','inconclusive',effort_minutes=5,updates={'public':Side('Copper','accepted','x')})

    def test_unknown_nonlead_decision_cannot_satisfy_supported_rule(self):
        case=record_department_decision(self.case,effort_minutes=4,evidence_root=self.root,decision_record=self.decision(self.case))
        self.assertIsNone(case.accepted_category)
        self.assertEqual(case.review_history[-1].outcome,'classification_deferred')
        self.assertIn('does not satisfy',case.review_history[-1].validation_error)
        self.assertEqual(case.staff_minutes,4)

    def test_missing_unvalidated_or_tampered_decision_remains_pending_with_effort(self):
        case=self.complete_case()
        missing=record_department_decision(case,effort_minutes=3,evidence_root=self.root,decision_record={'path':'missing.json','sha256':'0'*64})
        self.assertIsNone(missing.accepted_category);self.assertEqual(missing.staff_minutes,3)
        pointer=self.decision(case);record=json.loads((self.root/pointer['path']).read_text());record['validation']['status']='pending'
        pending=record_department_decision(case,effort_minutes=2,evidence_root=self.root,decision_record=self.artifact('pending.json',record))
        self.assertIsNone(pending.accepted_category)
        (self.root/pointer['path']).write_text('{}')
        tampered=record_department_decision(case,effort_minutes=2,evidence_root=self.root,decision_record=pointer)
        self.assertIsNone(tampered.accepted_category);self.assertIn('SHA256',tampered.review_history[-1].validation_error)

    def test_decision_must_match_case_and_current_evidence_state(self):
        case=self.complete_case();pointer=self.decision(case)
        for changed in [replace(case,case_id='different'),replace(case,baseline_as_of='2026-10-19'),replace(case,customer=Side('Copper','accepted','new-evidence'))]:
            result=record_department_decision(changed,effort_minutes=2,evidence_root=self.root,decision_record=pointer)
            self.assertIsNone(result.accepted_category)

    def test_required_side_evidence_file_must_exist_and_match(self):
        case=self.complete_case();pointer=self.decision(case)
        (self.root/'evidence-0.txt').unlink()
        result=record_department_decision(case,effort_minutes=2,evidence_root=self.root,decision_record=pointer)
        self.assertIsNone(result.accepted_category)

    def test_category_specific_one_side_rule_is_supported(self):
        case=replace(self.case,public=Side('Lead','accepted','synthetic-lead-proof'))
        case=record_department_decision(case,effort_minutes=2,evidence_root=self.root,decision_record=self.decision(case,'Lead'))
        self.assertFalse(fully_evidenced_pair(case));self.assertEqual(case.accepted_category,'Lead')

    def test_rejected_and_deferred_classification_reviews_keep_effort_and_history(self):
        self.assertTrue(eligible(self.case,'classification_review'))
        case=classification_review(self.case,'classification_rejected',effort_minutes=4)
        case=classification_review(case,'classification_deferred',effort_minutes=3)
        self.assertEqual((case.attempts,case.staff_minutes),(2,7))
        self.assertIsNone(case.accepted_category)
        self.assertEqual([e.outcome for e in case.review_history],['classification_rejected','classification_deferred'])

    def test_accepted_category_cannot_be_overwritten_or_double_counted(self):
        accepted=self.accept()
        with self.assertRaises(ValueError): record_department_decision(accepted,effort_minutes=3,evidence_root=self.root,decision_record=self.decision(accepted,'Lead'))
        self.assertEqual(accepted.accepted_category,'Non-Lead');self.assertEqual(len(accepted.review_history),1)

    def test_correction_requires_superseded_record_and_retains_both_decisions(self):
        accepted=self.accept();new_public=Side('Lead','accepted','synthetic-new-proof')
        rejected=correct_department_decision(accepted,effort_minutes=1,outcome='classification_rejected')
        self.assertEqual(rejected.accepted_category,'Non-Lead');self.assertEqual(rejected.staff_minutes,3)
        self.assertEqual(rejected.review_history[-1].outcome,'classification_rejected')
        target=replace(accepted,public=new_public)
        invalid=correct_department_decision(accepted,effort_minutes=3,evidence_root=self.root,
            decision_record=self.decision(target,'Lead',decision_id='new-decision'),corrected_sides={'public':new_public})
        self.assertEqual(invalid.accepted_category,'Non-Lead');self.assertEqual(invalid.public.reported_material,'Copper')
        pointer=self.decision(target,'Lead',decision_id='corrected-decision',correction=True)
        corrected=correct_department_decision(accepted,effort_minutes=3,evidence_root=self.root,
            decision_record=pointer,corrected_sides={'public':new_public})
        self.assertEqual(corrected.accepted_category,'Lead');self.assertEqual(corrected.staff_minutes,5)
        self.assertEqual([e.category_after for e in corrected.review_history],['Non-Lead','Lead'])
        self.assertEqual(corrected.review_history[-1].supersedes_decision_id,'synthetic-decision')
        self.assertEqual(corrected.review_history[-1].public_before.reported_material,'Copper')
        self.assertEqual(corrected.review_history[-1].public_after.reported_material,'Lead')

    def test_unknown_material_missing_effort_or_fake_boolean_cannot_accept(self):
        with self.assertRaises(ValueError): Side('Unknown','accepted','x')
        with self.assertRaises(ValueError): Side('Copper','accepted',None)
        with self.assertRaises(ValueError): classification_review(self.case,'classification_deferred',effort_minutes=None)
        with self.assertRaises(TypeError): record_department_decision(self.case,'Non-Lead',rules_confirmed=True,rule_ref='x',decision_ref='x',effort_minutes=1)

if __name__=='__main__': unittest.main()
