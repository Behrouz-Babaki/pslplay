from reloop.languages.rlp.grounding.block import BlockGrounder
from reloop.languages.rlp.logkb import PyDatalogLogKb

from DOBSS import *
from pyDatalogUtil import *
from LiftingAnalysis import LiftingAnalysis

from simple_matrices import *

numpy.set_printoptions(threshold=numpy.nan)

loadFacts("facts/simple_matrices.facts")

scenario(X)

for sname in X.data:
  print(sname)
  assertAll("activeScenario",[[sname]])

  logfile = open("logs/{0}.blocklp.log".format(sname),"w",0)
  
  print >> logfile, "DOBSS BLOCK LP"
  print >> logfile, "BEGIN GAME MATRIX"
  print >> logfile, gameMatrix(sname,X,Y,V,W)
  print >> logfile, "END GAME MATRIX"

  analyzer = LiftingAnalysis(logfile, dumpSingleMatrices = True, dumpBlockMatrix = True)
  solver = lambda : analyzer
  logkb = PyDatalogLogKb()
  grounder = BlockGrounder
  solve_dobss_block(grounder, logkb, solver)
  
  analyzer.subproblemLiftingAnalysis()
  
  logfile.close()
  retractAll("activeScenario",1)
