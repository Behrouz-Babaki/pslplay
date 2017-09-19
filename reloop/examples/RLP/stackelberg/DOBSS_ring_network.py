from reloop.languages.rlp.grounding.block import BlockGrounder
from reloop.languages.rlp.logkb import PyDatalogLogKb


from DOBSS import *
from pyDatalogUtil import *
from LiftingAnalysis import LiftingAnalysis

from ring_network import *

# Running DOBSS on a ring network model

loadFacts("facts/large_ring.facts")

logfile = open("logs/ring_network_large.log","w",0)

# Dump facts, action sets and game matrix into logfile
print >> logfile, "--- EDGES"
print >> logfile, edge(X,Y)
print >> logfile, "--- LEADER ACTIONS"
print >> logfile, leaderAction(X)
print >> logfile, "--- FOLLOWER ACTIONS"
print >> logfile, followerAction(X)
print >> logfile, "BEGIN GAME MATRIX"
print >> logfile, gameMatrix(X,Y,V,W)
print >> logfile, "END GAME MATRIX"

analyzer = LiftingAnalysis(logfile)
# lambda binding so that the solver can be reinstantiated within the model but in reality it stays the same
# instance all the time.
solver = lambda : analyzer
logkb = PyDatalogLogKb()
grounder = BlockGrounder

# build the model and analyze it
solve_dobss_subproblems(grounder, logkb, solver)
analyzer.liftingAnalysis()

logfile.close()
