import scipy.sparse as sp
import numpy as np
import reloop.utils.saucy as saucy

A = sp.coo_matrix([[1, 1, 1], [-1, 0, 0], [0, -1, 0], [1, 1, -1]])
b = sp.coo_matrix([1,0,0,-1]).T
c = sp.coo_matrix([0,0,1]).T

print "input LP:"
print "c: " + str(c.todense().T)
print "b: " + str(b.todense())
print "A: " + str(A.todense())

LA, Lb, Lc, LG, Lh, compresstime, Bcc = saucy.liftAbc(A, b, c, G=A, h=b, sparse=True, orbits=False)


print "lifted LP:"
print "lifted c: " + str(Lc.T)
print "Lb: " + str(Lb)
print "LA: " + str(LA.todense())
print "Lh: " + str(Lh)
print "LG: " + str(LG.todense())
print Bcc.todense()
