from scipy.io import mmread
import scipy.sparse as sp
import reloop.utils.saucy as saucy
import reloop.utils.saucywrapper as sw
import numpy as np


M = mmread("../data/graphs/piece_13481_4.mtx")

print M.shape

evid = np.loadtxt("../data/graphs/labels_vec.txt",delimiter=",", dtype = np.uintp)
print np.unique(evid)
print evid.shape


colors = sw.epSaucy(M.data.round(6).astype(np.float), M.row.astype(np.uintp), M.col.astype(np.uintp), evid.astype(np.uintp), np.int32(0));
print "var colors: ", colors[0:M.shape[0]]
print "edge colors: ", colors[M.shape[0]:]