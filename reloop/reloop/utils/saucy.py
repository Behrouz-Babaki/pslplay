import reloop.utils.saucywrapper as saucywrapper
import scipy.sparse as sp
import numpy as np
import time

def epBipartite(A, b, c, G=None, h=None, orbits=False):

	_, cmod = np.unique(np.array(c.todense()), return_inverse=True)
	_, bmod = np.unique(np.array(b.todense()), return_inverse=True)
	if h is not None:
		_, hmod = np.unique(np.array(h.todense()), return_inverse=True)
		hmod += np.max(bmod) + 1
		bmod = np.hstack((bmod, hmod))
	if G is not None:
		A = sp.vstack((A,G))
	# print "======++EPBIPARTITE"
	# print bmod.shape
	# print A.shape
	# print G.shape
	# print A.todense()
	# print bmod
	_, data = np.unique(A.data.round(6), return_inverse=True)
	
	colors = saucywrapper.epSaucyBipartite(
            data.astype(np.uintp), A.row.astype(np.uintp),
            A.col.astype(np.uintp), bmod.astype(np.uintp),
            cmod.astype(np.uintp), np.int32(0), orbits)
	
	n = cmod.shape[0]
	m = bmod.shape[0]
	
	# print m
	# print n
	# print colors
	_, ccols2 = np.unique(colors[m:(n + m)], return_inverse=True)
	_, rcols2 = np.unique(colors[0:m], return_inverse=True)
	return [rcols2, ccols2]


def liftAbc(Ar, br, cr, G=None, h=None, sparse=True, orbits=False, sumrefine=False):
	"""
	TODO

	:param Ar:
	:type Ar:
	:param br:
	:type br:
	:param cr:
	:type cr:
	:param sparse:
	:type sparse:
	:param orbits:
	:type orbits:
	:param sumrefine:
	:type sumrefine:

	:returns:
	"""
	eqs = False
	if G is not None and h is not None: eqs = True
	GC = None
	ho = None

	if sparse:
	    AC = Ar.tocoo()
	    if eqs:	GC = G.tocoo()
	else:
	    AC = sp.coo_matrix(Ar)
	    if eqs:	GC = sp.coo_matrix(G)

	starttime = time.clock()
	
	co = sp.lil_matrix(cr)
	bo = sp.lil_matrix(br)
	if eqs: 
		ho = sp.lil_matrix(h) 

	if sumrefine and not orbits:
	    saucycolors = sumRefinement(AA, cc)
	else:
	    [rcols, ccols2] = epBipartite(AC, bo, co, G=GC, h=ho, orbits=orbits)
	    
	print "refinement took: ", time.clock() - starttime, "seconds."

	n = cr.shape[0]
	m = br.shape[0]
	if eqs: o = h.shape[0]

	crows = np.array(range(n))
	bdata = np.ones(n, dtype=np.int)

	Bcc2 = sp.csr_matrix((bdata, np.vstack((crows, ccols2))), dtype=np.int).tocsr()
	
	if eqs:
		rcols2 = rcols[m:(m+o)] 
		rcols = rcols[0:m]
		_, rowfilter2 = np.unique(rcols2, return_index=True)

		LG2 = GC.tocsr()[rowfilter2, :] * Bcc2
		Lh = ho[rowfilter2].todense()
	else:
		LG2 = None
		Lh = None

	# print LG2.shape
	# print Lh.shape
	_, rowfilter = np.unique(rcols, return_index=True)
	LA2 = AC.tocsr()[rowfilter, :] * Bcc2
	Lb = bo[rowfilter].todense()
	Lc = (co.T * Bcc2).T
	
	compresstime = time.clock() - starttime
	LA2 = LA2.tocoo()
	Lc = Lc.todense()
	if eqs: 
		LG2 = LG2.tocoo() 
		return LA2, Lb, Lc, LG2, Lh, compresstime, Bcc2 
	else: 
		return LA2, Lb, Lc, None, None, compresstime, Bcc2