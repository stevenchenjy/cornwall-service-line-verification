from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from inventory_audit import material_state, gap, audit, address_key, expected_complete, repeated_record_diagnostics

def row(public='Unknown', customer='Unknown', address='1 Main St', zip_code='12520', category='Unknown'):
    return dict(current_public_side_sl=public,customer_sl_material=customer,street_address=address,zip_code=zip_code,sl_category=category)

class InventoryChecks(unittest.TestCase):
    def test_unknown_variants(self):
        self.assertEqual([material_state(v) for v in ['unknown',' UNKNOWN ','Unknown but could be lead','Unknown but unlikely lead']], ['unknown']*4)

    def test_missing_and_unmapped_not_known(self):
        self.assertEqual(material_state(None),'missing')
        self.assertEqual(material_state('new unrecognized material'),'unmapped')
        self.assertEqual(gap(row(customer=None)),'missing_material_field')

    def test_both_sides_matter(self):
        rows=[row(),row(customer='Copper'),row(public='Copper')]
        result=audit(rows)
        self.assertEqual(result['unknown_gap_buckets'],dict(both_unknown=1,public_unknown=1,customer_unknown=1))
        self.assertEqual(result['unknown_rows_needing_public_material'],2)
        self.assertEqual(result['resident_only_completion_raw_row_upper_bound'],1)

    def test_duplicate_groups_not_excess_rows(self):
        result=audit([row(),row(),row(),row(address='2 Main St'),row(address='2 Main St')])
        dup=result['exact_address_zip_duplicates']
        self.assertEqual((dup['repeated_key_groups'],dup['rows_in_repeated_groups'],dup['excess_rows']),(2,5,3))
        self.assertEqual(result['raw_rows'],5)

    def test_preserve_apartments_and_missing_keys(self):
        self.assertNotEqual(address_key(row(address='1 Main St Apt 1'),True),address_key(row(address='1 Main St Apt 2'),True))
        self.assertIsNone(address_key(row(address='')))

    def test_case_normalization_without_fuzzy_merge(self):
        self.assertEqual(address_key(row(address=' 1  MAIN St '),True),address_key(row(address='1 Main St'),True))
        self.assertNotEqual(address_key(row(address='1 Main Street'),True),address_key(row(address='1 Main St'),True))

    def test_explicit_complete_probability_and_cap(self):
        self.assertEqual(expected_complete(10,20,.6),6)
        with self.assertRaises(ValueError): expected_complete(10,20,None)
        with self.assertRaises(ValueError): expected_complete(21,20,.6)

    def test_nonunknown_inconsistency_not_silent(self):
        result=audit([row(category='Non-Lead')])
        self.assertEqual(result['unknown_category_rows'],0)
        self.assertEqual(result['nonunknown_category_rows_with_unknown_or_missing_material'],1)

    def test_repeated_groups_distinguish_identical_and_conflicting_records(self):
        rows=[row(),row(),row(address='2 Main St'),row(address='2 Main St',category='Non-Lead')]
        result=repeated_record_diagnostics(rows)
        self.assertEqual(result['repeated_groups'],2)
        self.assertEqual(result['identical_payload_groups'],1)
        self.assertEqual(result['identical_material_method_category_groups'],1)
        self.assertEqual(result['differing_category_groups'],1)
        self.assertEqual(len(rows),4)

if __name__ == '__main__':
    unittest.main()
