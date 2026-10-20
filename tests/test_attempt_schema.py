"""Synthetic workflow events must survive the draft JSON Schema intake contract."""
from copy import deepcopy
from dataclasses import asdict, replace
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError

import test_workflow as fixtures
from verification_workflow import Side, correct_department_decision


class AttemptSchemaChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / 'data/schema/verification-attempt-log.schema.json'
        schema = json.loads(path.read_text())
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema)

    def setUp(self):
        self.fixture = fixtures.WorkflowChecks()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.accepted = self.fixture.accept()

    def attempt_record(self, result):
        """Test mapping only: not a department importer or an acceptance policy."""
        event = result.review_history[-1]
        return dict(
            attempt_id='synthetic-correction-attempt', case_id=result.case_id,
            previous_attempt_id='synthetic-initial-acceptance', pws_id=result.pws_id,
            baseline_as_of=result.baseline_as_of, attempt_date='2026-10-20',
            initial_public=asdict(event.public_before),
            initial_customer=asdict(event.customer_before),
            reported_category_before=event.previous_category,
            action=event.action, outcome=event.outcome,
            public_after=asdict(event.public_after), customer_after=asdict(event.customer_after),
            accepted_category_after=event.category_after,
            acceptance_rule_ref=result.acceptance_rule_ref,
            decision_ref=result.acceptance_decision_ref,
            follow_up_required=event.outcome != 'classification_accepted',
            selection_reason='Synthetic contract regression; no observed local data',
            preparation_minutes=None, travel_minutes=None, contact_field_minutes=None,
            administration_review_minutes=event.effort_minutes,
            supersedes_decision_id=event.supersedes_decision_id,
            correction_reason=event.correction_reason,
            validation_error=event.validation_error,
            validation_status='validated' if event.outcome == 'classification_accepted' else 'pending',
        )

    def accepted_correction(self):
        new_public = Side('Lead', 'accepted', 'synthetic-corrected-evidence')
        target = replace(self.accepted, public=new_public)
        pointer = self.fixture.decision(
            target, 'Lead', decision_id='synthetic-corrected-decision', correction=True)
        return correct_department_decision(
            self.accepted, effort_minutes=3, evidence_root=self.fixture.root,
            decision_record=pointer, corrected_sides={'public': new_public})

    def test_deferred_correction_preserves_effort_and_nullable_metadata(self):
        result = correct_department_decision(self.accepted, effort_minutes=3)
        record = self.attempt_record(result)
        self.assertEqual(record['outcome'], 'classification_deferred')
        self.assertEqual(record['accepted_category_after'], self.accepted.accepted_category)
        self.assertEqual(result.staff_minutes, self.accepted.staff_minutes + 3)
        self.assertEqual(record['administration_review_minutes'], 3)
        self.assertIsNone(record['supersedes_decision_id'])
        self.assertIsNone(record['correction_reason'])
        self.assertTrue(record['validation_error'])
        self.validator.validate(record)

        partial = deepcopy(record)
        partial['supersedes_decision_id'] = self.accepted.acceptance_decision_ref
        self.validator.validate(partial)
        absent = deepcopy(record)
        absent.pop('supersedes_decision_id')
        absent.pop('correction_reason')
        self.validator.validate(absent)

    def test_rejected_correction_retains_category_and_effort_without_invented_metadata(self):
        result = correct_department_decision(
            self.accepted, effort_minutes=4, outcome='classification_rejected')
        record = self.attempt_record(result)
        self.assertEqual(record['accepted_category_after'], self.accepted.accepted_category)
        self.assertEqual(result.staff_minutes, self.accepted.staff_minutes + 4)
        self.assertIsNone(record['supersedes_decision_id'])
        self.assertIsNone(record['correction_reason'])
        self.validator.validate(record)

    def test_accepted_correction_still_requires_nonempty_metadata(self):
        record = self.attempt_record(self.accepted_correction())
        self.assertEqual(record['outcome'], 'classification_accepted')
        self.validator.validate(record)
        for key in ('supersedes_decision_id', 'correction_reason'):
            for bad_value in (None, ''):
                with self.subTest(key=key, bad_value=bad_value):
                    invalid = deepcopy(record)
                    invalid[key] = bad_value
                    with self.assertRaises(ValidationError):
                        self.validator.validate(invalid)
            with self.subTest(key=key, bad_value='absent'):
                invalid = deepcopy(record)
                invalid.pop(key)
                with self.assertRaises(ValidationError):
                    self.validator.validate(invalid)


if __name__ == '__main__':
    unittest.main()
