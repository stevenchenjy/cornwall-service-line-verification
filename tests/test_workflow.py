import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from verification_workflow import Case, Side, eligible, apply_attempt, fully_evidenced_pair, record_department_decision


class WorkflowChecks(unittest.TestCase):
    def test_both_unknown_can_follow_records_then_resident_sequence(self):
        case=Case()
        self.assertTrue(eligible(case,'public_records'))
        self.assertTrue(eligible(case,'resident_assisted'))
        case=apply_attempt(case,'public_records','evidence_returned',effort_minutes=10,
            updates={'public':Side('Copper','accepted','synthetic-record-review')})
        case=apply_attempt(case,'resident_assisted','evidence_returned',effort_minutes=12,
            updates={'customer':Side('Copper','submitted','synthetic-submission')})
        self.assertFalse(fully_evidenced_pair(case))
        self.assertIsNone(case.accepted_category)
        case=apply_attempt(case,'resident_assisted','evidence_returned',effort_minutes=3,
            updates={'customer':Side('Copper','accepted','synthetic-acceptance')})
        self.assertTrue(fully_evidenced_pair(case))
        self.assertIsNone(case.accepted_category)
        case=record_department_decision(case,'Non-Lead',rules_confirmed=True,
            rule_ref='synthetic-rule',decision_ref='synthetic-decision',effort_minutes=2)
        self.assertEqual(case.accepted_category,'Non-Lead')
        self.assertEqual((case.attempts,case.staff_minutes),(4,27))
        self.assertFalse(eligible(case,'joint_field_visit'))

    def test_known_material_without_accepted_evidence_remains_eligible(self):
        case=Case(public=Side('Copper'),customer=Side('Copper'))
        self.assertTrue(eligible(case,'public_records'))
        self.assertTrue(eligible(case,'resident_assisted'))
        self.assertFalse(fully_evidenced_pair(case))

    def test_nonresponse_rejected_evidence_and_retry_keep_full_effort(self):
        case=apply_attempt(Case(),'resident_assisted','no_response',effort_minutes=5)
        case=apply_attempt(case,'resident_assisted','evidence_returned',effort_minutes=8,
            updates={'customer':Side('Copper','rejected','synthetic-blurry-photo')})
        self.assertTrue(eligible(case,'resident_assisted'))
        self.assertEqual((case.attempts,case.staff_minutes),(2,13))
        self.assertIsNone(case.accepted_category)

    def test_actions_cannot_rewrite_other_side_or_resolve_failed_contact(self):
        with self.assertRaises(ValueError):
            apply_attempt(Case(),'resident_assisted','evidence_returned',effort_minutes=5,
                updates={'public':Side('Copper','accepted','x')})
        with self.assertRaises(ValueError):
            apply_attempt(Case(),'public_records','inconclusive',effort_minutes=5,
                updates={'public':Side('Copper','accepted','x')})

    def test_acceptance_requires_references_and_never_invented_two_side_rule(self):
        with self.assertRaises(ValueError):
            record_department_decision(Case(),'Non-Lead',rules_confirmed=False,rule_ref='',decision_ref='',effort_minutes=1)
        # A synthetic external rule may resolve a category with one side unknown.
        case=record_department_decision(Case(public=Side('Lead','accepted','synthetic-proof')),
            'Lead',rules_confirmed=True,rule_ref='synthetic-one-side-rule',decision_ref='synthetic-decision',effort_minutes=1)
        self.assertFalse(fully_evidenced_pair(case))
        self.assertEqual(case.accepted_category,'Lead')

    def test_unknown_material_cannot_gain_accepted_side_evidence(self):
        with self.assertRaises(ValueError): Side('Unknown','accepted','x')
        with self.assertRaises(ValueError): Side('Copper','accepted',None)

if __name__=='__main__':
    unittest.main()
