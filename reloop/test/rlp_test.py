import unittest
from reloop.languages.rlp import SubSymbol, sub_symbols, numeric_predicate, NumericPredicate,\
    boolean_predicate, BooleanPredicate, RlpPredicate


class TestRlp(unittest.TestCase):
    def test_subsymbols(self):
        a, b, x = sub_symbols('a', 'B', 'XX')

        self.assertEqual(a, SubSymbol('a'))
        self.assertEqual(b, SubSymbol('B'))
        self.assertEqual(x, SubSymbol('XX'))

        a = sub_symbols('a')
        self.assertEqual(a, SubSymbol('a'))

    def test_numeric_predicate(self):
        pred = numeric_predicate("pred", 2)

        self.assertEqual(pred.arity, 2)
        self.assertEqual(pred.name, "pred")
        self.assertFalse(pred.isReloopVariable)

        pred_inst1 = pred(1,2)
        self.assertIsInstance(pred_inst1, NumericPredicate)
        pred_inst2 = pred(2,2)
        self.assertNotEqual(pred_inst1, pred_inst2)

        other = numeric_predicate("pred", 2)
        self.assertEqual(other, pred)

        self.assertRaises(ValueError, numeric_predicate, "pred", -1)
        try:
            numeric_predicate("pred", 0)
        except:
            self.fail("Creating a 0-arity numeric predicate failed!")

        pred = numeric_predicate("pred", 0)
        self.assertIsInstance(pred(), RlpPredicate)

    def test_boolean_predicate(self):
        pred = boolean_predicate("pred", 2)

        self.assertEqual(pred.arity, 2)
        self.assertEqual(pred.name, "pred")
        self.assertFalse(pred.isReloopVariable)

        pred_inst1 = pred(1,2)
        self.assertIsInstance(pred_inst1, BooleanPredicate)
        pred_inst2 = pred(2,2)
        self.assertNotEqual(pred_inst1, pred_inst2)

        other = boolean_predicate("pred", 2)
        self.assertEqual(other, pred)

        self.assertRaises(ValueError, boolean_predicate, "pred", -1)
        self.assertRaises(ValueError, boolean_predicate, "pred", 0)