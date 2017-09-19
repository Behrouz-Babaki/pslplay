=======
Glpk2Py
=======


.. cpp:enum::  glpk2py::filetype
	
     The Format of a given file

    =====  =====  ===========
    Name   Value  Description
    =====  =====  ===========
    MPS      0    Given file is in the MPS format 
    LP       1    Given file is in the LP format  
    =====  =====  ===========

.. cpp:enum::  glpkl2py::bounds

     Flags, which indicate the different bounds to be calculated for given LP.
     For instance if UPPER is set the function getMatrix() will calculate the upper bounds for the specified LP object.

    =======  =====  ===========
    Name     Value  Description
    =======  =====  ===========
    UPPER    0      Upper Bounds ax > b
    LOWER    1      Lower Bounds ax < b
    EQUAL    2      Fixed Bounds ax = b
    UNBOUND  3      Unbound ax < 0
    =======  =====  ===========

.. cpp:enum::  glpk2py::scaling

     Flags used for distinguishing between the different scaling types to be used by the defined functions.

    =======  =====  ===========
    Name     Value  Description
    =======  =====  ===========
    GEOMEAN    0    Geometric mean scaling
    EQUILIB    1    Equilibration scaling
    =======  =====  ===========


.. cpp:function:: void glpk2py::openLP(const std::string &fname, int format) 

     Opens the LP by creating a glpk problem object and assigning the given file to it \n
     Furthermore extracts the number of columns and rows of the opened LP and assigns the values to global variables

    :param fname: The name of the file to be opened
    :type fname: string.
    :param format: The filetype of given file either MPS or LP are valid (see enum filetype)
    :type format: int.


.. cpp:function:: void glpk2py::closeLP(void)

     Closes LP by calling the destructor of glpk, which deallocates all memory used by the corresponding problem object iff the constructor was called in openLP\n
     The call of glp_free_env() frees all resources used by GLPK routines


.. cpp:function:: vector<double> glpk2py::getMatrix(bounds boundquery, int scaled)

     Computes a Matrix depending on the boundquery argument (see bounds)

    :param boundquery: Flag to determine, which inquality is going to be calculated
    :type boundquery: bounds.
    :param scaled: An integer, which indicates a scaled matrix(LP)
    :type scaled: int.
    :returns: A vector of the type double and 4 x n dimensions, which contains the data.

    Computes a Matrix depending on the boundquery Argument (see bounds) 
    UPPER --Calculates the Upper bounds of a given LP and returns it as a vector
    LOWER --Calculates the Lower bounds of a given LP and returns it as a vector
    EQUAL -- Calculates fixed variables of a given LP and returns it as a vector
    UNBOUND -- Calculates unbound variables of a given LP

.. cpp:function:: vector<double> glpk2py::getObjective(int scaled)
    
     Calculates the objective of a given LP

    :param scaled: An integer, which indicates a scaled matrix(LP)
    :type scaled: int.
    :returns:  The Objective of an opened LP as vector of type double.

    Creates a new vector object with the size of the number of columns of given lp then iterates over this vector and 
    calculates the objective coefficient at the i-th column of the lp (problem) object. If the problem is scaled 
    the scale factor s is set to the current scaled factor and the current position of the matrix of the lp object. 

.. cpp:function:: void glpk2py::doScaling(scaling sctype)

     Wrapper function for the glp scaling method, which does the actual scaling of the given lp.

    :param sctype: Flag, which determines the type of scaling to be executed for a given LP
    :type sctype: scaling.


.. cpp:function:: void glpk2py::solve()

     Solves the given LP with an off-the-shelf LP-Solver for instance using the Gnu GLPK

.. highlight:: cpp
.. literalinclude:: ../../reloop/utils/io/glpk2py.cpp