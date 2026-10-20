from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_language import language_regressions


class LanguageRegressionChecks(unittest.TestCase):
    def test_prior_language_regression_is_rejected(self):
        self.assertEqual(language_regressions('English heading\n\u7814\u7a76'),
                         [(2, 'U+7814'), (2, 'U+7A76')])

    def test_english_with_names_and_scientific_notation_is_allowed(self):
        self.assertEqual(language_regressions('Cornwall-on-Hudson; Jose\u0301; 365/366 days; \u00b1d/2 gallons; \u03bcg/L.'), [])
