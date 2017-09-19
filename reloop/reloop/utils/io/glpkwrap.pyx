## @package wrapper
#Documentation for this module.
#
#


from cython.operator cimport preincrement as inc
import numpy as np
cimport numpy as np

#there is a bug with typing certain variables. To circumvent it we need to define our own type and pass it to the compiler otherwise the function will pass garbage to the c++ function
ctypedef np.uintp_t itype_t


cdef extern from "<vector>" namespace "std":
    cdef cppclass vector[T]:
        cppclass iterator:
            T operator*()
            iterator operator++()
            bint operator==(iterator)
            bint operator!=(iterator)
        vector()
        void push_back(T&)
        T& operator[](int)
        T& at(int)
        iterator begin()
        iterator end()
        int size()

cdef extern from "glpk2py.h":
 
    cdef enum bounds:      
        UPPER
        LOWER
        EQUAL
        UNBOUND

    cdef enum scaling:     
        GEOMMEAN
        EQUILIB

    void openLP(const char* fname, int format_);
    void closeLP();
    vector[double] getMatrix(bounds boundquery,int scaled);
    vector[double] getObjective(int scaled);
    void doScaling(scaling sctype);
    void solve();


##Calls C++ code which opens a linear Program to solve given problem in specified file
#
#@param fname -- The path of a specified file, which is subject to solving
#@param format -- A specified format as how to solve the given LP ?

def openLP_Py(fname,format_):
   
    openLP(fname,format_)

## Calls function closeLP from glpk2py.cpp (see closeLP)
#
def closeLP_Py():
    closeLP()

##Computes the Upper Bounds for a given LP and returns it as a multi-dimensional array
#
#
#@param scaled  Flag, which indicates a scaled matrix    
def getMatrix_Upper(scaled):
   
    cdef vector[double] res
    res = getMatrix(UPPER,scaled)
    
    i = res.size()
    d = i/4
    cdef np.ndarray result = np.zeros([4,i/4],dtype=np.double)

    for x in range(0,d):
        result[0,x] = res[x]
        result[1,x] = res[x+d]
        result[2,x] = res[x+d*2]
        result[3,x] = res[x+d*3]

    return result

##Computes the Lower Bounds for a given LP and returns it as a multi-dimensional array
#
#@param    scaled Flag, which indicates a scaled matrix   
def getMatrix_Lower(scaled):
 
    cdef vector[double] res
    res = getMatrix(LOWER,scaled)

    i = res.size()
    d = i/4
    cdef np.ndarray result = np.zeros([4,i/4],dtype=np.double)

    for x in range(0,d):
        result[0,x] = res[x]
        result[1,x] = res[x+d]
        result[2,x] = res[x+d*2]
        result[3,x] = res[x+d*3]

    return result

##Computes the Equality constraints of given LP and returns it as a multi-dimensional array
#
#@param    scaled Flag, which indicates a scaled matrix 
def getMatrix_Equal(scaled):

    cdef vector[double] res
    res = getMatrix(EQUAL,scaled)

    i = res.size()
    d = i/4
    cdef np.ndarray result = np.zeros([4,i/4],dtype=np.double)

    for x in range(0,d):
        result[0,x] = res[x]
        result[1,x] = res[x+d]
        result[2,x] = res[x+d*2]
        result[3,x] = res[x+d*3]

    return result

def getMatrix_Unbound(scaled):

    cdef vector[double] res
    res = getMatrix(UNBOUND,scaled)

    i = res.size()
    d = i/4
    cdef np.ndarray result = np.zeros([4,i/4],dtype=np.double)

    for x in range(0,d):
        result[0,x] = res[x]
        result[1,x] = res[x+d]
        result[2,x] = res[x+d*2]
        result[3,x] = res[x+d*3]

    return result

##Calls the function getObjective from glpk2py.cpp and returns the objectives as one-dimensional array (see getObjective.cpp)
#
#@param scaled Flag, which indicates a scaled matrix
def getObjective_Py(scaled):
    cdef vector[double] res = getObjective(scaled)
    #Instantiate numpy Array and get size of objective
    i = res.size()
    cdef np.ndarray result = np.empty(i)

    for x in range(0,i):
     result[x] = res[x]
  
    return result

def doScaling_Py(sctype):
    if sctype == 7:
        doScaling(EQUILIB)
    else:
        doScaling(GEOMMEAN)

def solve_Py():
    solve()
