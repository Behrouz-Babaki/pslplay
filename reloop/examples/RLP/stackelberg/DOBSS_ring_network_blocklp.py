from reloop.languages.rlp.grounding.block import BlockGrounder
from reloop.languages.rlp.logkb import PyDatalogLogKb


from DOBSS import *
from pyDatalogUtil import *
from LiftingAnalysis import LiftingAnalysis

from ring_network import *

import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s')

# from pyDatalog import pyEngine
# pyEngine.Logging = True

loadFacts("facts/large_ring.facts")

logfile = open("logs/ring_network_large.blocklp.log","w",0)

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
solver = lambda : analyzer
logkb = PyDatalogLogKb()
grounder = BlockGrounder

solve_dobss_block(grounder, logkb, solver)

analyzer.subproblemLiftingAnalysis()

logfile.close()
