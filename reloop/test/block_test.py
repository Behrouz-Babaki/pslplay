import unittest
from reloop.languages.rlp.grounding.block import BlockGrounder
from reloop.solvers.lpsolver import CvxoptSolver



class TestBlockGrounder(unittest.TestCase):
    def test_pydatalog(self):
        from pyDatalog import pyDatalog
        from examples.RLP import maxflow_example
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
        grounder = BlockGrounder(logkb)

        solver = CvxoptSolver()
        model = maxflow_example.maxflow(grounder, solver)
        self.assertEqual(model, 0, "PyDataLog Blockgrounding Failed")

    def test_postgres(self):
        from examples.RLP import maxflow_example
        from reloop.languages.rlp.logkb import PostgreSQLKb

        db_name= "reloop"
        db_user = "reloop"
        db_password="reloop"

        logkb = PostgreSQLKb(db_name, db_user, db_password)
        grounder = BlockGrounder(logkb)
        solver = CvxoptSolver()
        model = maxflow_example.maxflow(grounder, solver)
        self.assertEqual(model, 0, "PostgreSQL Blockgrounding Failed")

    def test_prolog(self):
        from examples.RLP import maxflow_example
        from reloop.languages.rlp.logkb import ProbLogKB

        logkb = ProbLogKB("../examples/RLP/maxflow_prolog.pl")
        grounder = BlockGrounder(logkb)
        solver = CvxoptSolver()

        model = maxflow_example.maxflow(grounder, solver)
        self.assertEqual(model, 0, "Prolog Blockgrounding Failed")

    def test_sudoku(self):
        from pyDatalog import pyDatalog
        from examples.RLP import sudoku_example
        from reloop.languages.rlp.logkb import PyDatalogLogKb

        for u in range(1, 10):
            pyDatalog.assert_fact('num', u)

        for u in range(1, 4):
            pyDatalog.assert_fact('boxind', u)

        pyDatalog.assert_fact('initial', 1, 1, 5)
        pyDatalog.assert_fact('initial', 2, 1, 6)
        pyDatalog.assert_fact('initial', 4, 1, 8)
        pyDatalog.assert_fact('initial', 5, 1, 4)
        pyDatalog.assert_fact('initial', 6, 1, 7)
        pyDatalog.assert_fact('initial', 1, 2, 3)
        pyDatalog.assert_fact('initial', 3, 2, 9)
        pyDatalog.assert_fact('initial', 7, 2, 6)
        pyDatalog.assert_fact('initial', 3, 3, 8)
        pyDatalog.assert_fact('initial', 2, 4, 1)
        pyDatalog.assert_fact('initial', 5, 4, 8)
        pyDatalog.assert_fact('initial', 8, 4, 4)
        pyDatalog.assert_fact('initial', 1, 5, 7)
        pyDatalog.assert_fact('initial', 2, 5, 9)
        pyDatalog.assert_fact('initial', 4, 5, 6)
        pyDatalog.assert_fact('initial', 6, 5, 2)
        pyDatalog.assert_fact('initial', 8, 5, 1)
        pyDatalog.assert_fact('initial', 9, 5, 8)
        pyDatalog.assert_fact('initial', 2, 6, 5)
        pyDatalog.assert_fact('initial', 5, 6, 3)
        pyDatalog.assert_fact('initial', 8, 6, 9)
        pyDatalog.assert_fact('initial', 7, 7, 2)
        pyDatalog.assert_fact('initial', 3, 8, 6)
        pyDatalog.assert_fact('initial', 7, 8, 8)
        pyDatalog.assert_fact('initial', 9, 8, 7)
        pyDatalog.assert_fact('initial', 4, 9, 3)
        pyDatalog.assert_fact('initial', 5, 9, 1)
        pyDatalog.assert_fact('initial', 6, 9, 6)
        pyDatalog.assert_fact('initial', 8, 9, 5)

        pyDatalog.load("""
            box(I, J, U, V) <= boxind(U) & boxind(V) & num(I) & num(J) & (I > (U-1)*3) & (I <= U*3) & (J > (V-1)*3) & (J <= V*3)
        """)

        logkb = PyDatalogLogKb()
        grounder = BlockGrounder(logkb)
        # Note: CVXOPT needs to be compiled with glpk support. See the CVXOPT documentation.
        solver = CvxoptSolver(solver_solver='glpk')

        model = sudoku_example.sudoku(grounder, solver)

        self.assertEqual(model, 0, "ERROR : Sudoku couldn't be solved")


if __name__ == '__main__':
    unittest.main()