import reloop.utils.io.glpkwrap as glpkwrap
import scipy.sparse as sp
import numpy as np

UPPER = 3
LOWER = 2
EQUAL = 5
UNBOUND = 1
GEOMMEAN = 6
EQUILIB = 7

def readLP(fname, scaled, ftype):
    """
     TODO: write me.

    :param fname: The name of a given file, which contains the LP
    :type fname: str.
    :param scaled: scaled An integeftype The type of the given problem (mostly LPs)r value, which indicates a scaling/scaled LP (?)
    :type scaled: int.
    :param ftype: ftype The type of the given problem (mostly LPs)
    :type ftype: str.
    :returns:  The n-tuple  [xopt, timeground, timelift, compresstime, shapeR0, shapeR1,shapeC0, shapeC1]:: 

            xopt --
            timeground -- 
            timelift --
            compresstime --
            shapeR0 --
            shapeR1 --
            shapeC0 --
            shapeC1 --

     >>> print loadNsolve('aircraft.gz.mts.lp',0,'LP')
     aircraft.gz.mts.lp :  [4.140719000000001, 0.393192, 0.37750799999999973, 7517, 57, 15025, 105]


    """  
    A = None
    b = None
    G = None
    h = None
    e = False
    openLP(fname,np.int32(ftype))
    if scaled == 1: doScaling(EQUILIB)
    lpmatrix = getMatrix_Upper(scaled) 
    nelms = np.int(lpmatrix[2,0])
    if nelms > 0:
        [A, b] = extract_matrix(lpmatrix)
        e = True
    lpmatrix = getMatrix_Lower(scaled)
    nelms = np.int(lpmatrix[2,0])
    if nelms > 0:
        [AA, bb] = extract_matrix(lpmatrix)
        if e:
            A = sp.vstack((A,-AA))
            b = np.hstack((b,-bb))
        else:
            A = -AA
            b = -bb
            e = True
    lpmatrix = getMatrix_Equal(scaled)
    nelms = np.int(lpmatrix[2,0])
    if nelms > 0:
        [G, h] = extract_matrix(lpmatrix)
    b = np.matrix(b)
    b.shape = (b.shape[1],1)
    b = sp.coo_matrix(b)
    if not (h is None):
        h = np.matrix(h)
        h.shape = (h.shape[1],1)
        h = sp.coo_matrix(h)
        print G.shape
        print h.shape
    c = getObjective(scaled)
    c.shape = (len(c),1)
    c = sp.coo_matrix(c)
    return A, b, c, G, h

def openLP(fname,ftype):
    """
    Calls C++ code which opens a linear Program to solve given problem in specified file.
    
    :param fname: The path of a specified file, which is subject to solving
    :type fname: str.
    :param ftype: A specified format as how to solve the given LP
    :type ftype: int.
    """
    glpkwrap.openLP_Py(fname,ftype)

def extract_matrix(lpmatrix):
    """
    Extracts a coordinate matrix from a given array with exactly 4 rows

    :param lpmatrix: An array with four rows. The first two rows being the row and column coordinates of the matrix to be extracted and the third row being the data for the respective coordinates. Fourth Row TODO

    :returns: a tuple (A,b)

            A -- The matrix extracted from lpmatrix!
            b -- the corresponding data vector.

    This function is heavily dependant on the number of the rows of given lpmatrix. Four rows are necessary for this function to be properly executed.

    >>> print extract_matrix(lpmatrix)
    A,b
    """


    ncols = np.int(lpmatrix[0,0])
    nrows = np.int(lpmatrix[1,0])
    nelms = np.int(lpmatrix[2,0])
    print nelms, ncols, nrows    
    i = np.array(lpmatrix[1,1:(nelms+1)], dtype = np.int) 
    j = np.array(lpmatrix[0,1:(nelms+1)], dtype = np.int) - 1
    d = lpmatrix[2,1:(nelms+1)]
    lb = np.int(lpmatrix[3,0]) + 1
    b = lpmatrix[3,1:lb]
    A = sp.coo_matrix((d, (i,j)), shape=(nrows, ncols))
    return [A, b]
 
def getMatrix_Upper(scaled):
    """
    Computes the Upper Bounds for a given LP and returns it as a multi-dimensional array
        Ax > b

    :param scaled: Flag, which indicates a scaled LP   
    :type scaled: int.

    :returns:
    """
    return glpkwrap.getMatrix_Upper(scaled)

def getMatrix_Lower(scaled):
    """
    Computes the Lower Bounds for a given LP and returns it as a multi-dimensional array
        Ax < b

    :param scaled: Flag, which indicates a scaled LP   
    :type scaled: int.

    :returns:
    """
    return glpkwrap.getMatrix_Lower(scaled)

def getMatrix_Equal(scaled):
    """
    TODO
        Ax = b

    :param scaled: Flag, which indicates a scaled LP   
    :type scaled: int.

    :returns:
    """

    return glpkwrap.getMatrix_Equal(scaled)

def getMatrix_Unbound(scaled):
    """
    Computes Unbound variables of given LP
        Ax < 0

    :param scaled: Flag, which indicates a scaled LP   
    :type scaled: int.

    :returns:
    """
    return glpkwrap.getMatrix_Unbound(scaled)

def getObjective(scaled):
    """
    Calls the function getObjective from glpk2py.cpp and returns the objectives as one-dimensional array (see getObjective.cpp)

    :param scaled: Flag, which indicates a scaled LP   
    :type scaled: int.

    :returns: The objective of a given lp as numpy array
    """
    return glpkwrap.getObjective_Py(scaled)
def solve():
    glpkwrap.solve_Py()
def doScaling(sctype):
     glpkwrap.doScaling_Py(sctype)
def closeLP():
    glpkwrap.closeLP_Py()
