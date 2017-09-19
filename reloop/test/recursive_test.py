import unittest
from reloop.languages.rlp.grounding.recursive import RecursiveGrounder
from reloop.solvers.lpsolver import CvxoptSolver
from examples.RLP import maxflow_example

class TestRecursiveGrounder(unittest.TestCase):

    def test_pydatalog(self):
        from pyDatalog import pyDatalog
        from reloop.languages.rlp.logkb import PyDatalogLogKb

        pyDatalog.assert_fact('node', 'a')
        pyDatalog.assert_fact('node', 'b')
        pyDatalog.assert_fact('node', 'c')
        pyDatalog.assert_fact('node', 'd')
        pyDatalog.assert_fact('node', 'e')
        pyDatalog.assert_fact('node', 'f')
        pyDatalog.assert_fact('node', 'g')

        pyDatalog.assert_fact('edge', 'a', 'b')
        pyDatalog.assert_fact('edge', 'a', 'c')
        pyDatalog.assert_fact('edge', 'b', 'd')
        pyDatalog.assert_fact('edge', 'b', 'e')
        pyDatalog.assert_fact('edge', 'c', 'd')
        pyDatalog.assert_fact('edge', 'c', 'f')
        pyDatalog.assert_fact('edge', 'd', 'e')
        pyDatalog.assert_fact('edge', 'd', 'f')
        pyDatalog.assert_fact('edge', 'e', 'g')
        pyDatalog.assert_fact('edge', 'f', 'g')

        pyDatalog.assert_fact('source','a')
        pyDatalog.assert_fact('target', 'g')

        pyDatalog.assert_fact('cost', 'a', 'b', 50 )
        pyDatalog.assert_fact('cost', 'a', 'c', 100)
        pyDatalog.assert_fact('cost', 'b', 'd', 40 )
        pyDatalog.assert_fact('cost', 'b', 'e', 20 )
        pyDatalog.assert_fact('cost', 'c', 'd', 60 )
        pyDatalog.assert_fact('cost', 'c', 'f', 20 )
        pyDatalog.assert_fact('cost', 'd', 'e', 50 )
        pyDatalog.assert_fact('cost', 'd', 'f', 60 )
        pyDatalog.assert_fact('cost', 'e', 'g', 70 )
        pyDatalog.assert_fact('cost', 'f', 'g', 70 )

        logkb = PyDatalogLogKb()
        grounder = RecursiveGrounder(logkb)

        solver = CvxoptSolver()
        model = maxflow_example.maxflow(grounder, solver)
        self.assertEqual(model, 0, "PyDataLog Recursive Failed")

    def test_postgres(self):
        from reloop.languages.rlp.logkb import PostgreSQLKb

        db_name= "reloop"
        db_user = "reloop"
        db_password="reloop"

        logkb = PostgreSQLKb(db_name, db_user, db_password)
        grounder = RecursiveGrounder(logkb)
        solver = CvxoptSolver()
        model = maxflow_example.maxflow(grounder, solver)
        self.assertEqual(model, 0, "PostgreSQL Recursive Failed")

    def test_prolog(self):
        from reloop.languages.rlp.logkb import ProbLogKB

        logkb = ProbLogKB("../examples/RLP/maxflow_prolog.pl")
        grounder = RecursiveGrounder(logkb)
        solver = CvxoptSolver()

        model = maxflow_example.maxflow(grounder, solver)
        self.assertEqual(model, 0, "Prolog Recursive Failed")

    def test_swipl(self):
        from pyswip import Prolog
        from reloop.languages.rlp.logkb import PrologKB
        prolog = Prolog()

        prolog.consult("../examples/RLP/maxflow_swipl.pl")
        logkb = PrologKB(prolog)
        # BlockGrounding not supported yet
        grounder = RecursiveGrounder(logkb)
        solver = CvxoptSolver()
        model = maxflow_example.maxflow(grounder, solver)
        self.assertEqual(model, 0, "SWI-Prolog Recursive Failed")

    def test_sudoku(self):
        pass
if __name__ == '__main__':
    unittest.main()