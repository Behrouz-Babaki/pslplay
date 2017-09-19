from reloop.languages.rlp import *
from reloop.languages.rlp.grounding.block import BlockGrounder
from reloop.languages.rlp.logkb import PyDatalogLogKb
from reloop.solvers.lpsolver import CvxoptSolver
import sudoku_example


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

sudoku_example.sudoku(grounder, solver)