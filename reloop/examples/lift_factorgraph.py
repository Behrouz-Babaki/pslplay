import scipy.sparse as sp
import numpy as np
import reloop.utils.saucy as saucy

A = sp.coo_matrix([[1, 2, 0], [0, 2, 1]])
b = sp.coo_matrix([0,0]).T
c = sp.coo_matrix([1,0,1]).T
[rowpart, colpart] = saucy.epBipartite(A, b, c, 1)
print "==="
print "row classes: ", rowpart
print "column classes: ", colpart 