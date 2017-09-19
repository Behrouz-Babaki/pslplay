/*! \file */ 

#include <limits>
#include <vector>
#include<iostream>
#include<assert.h>
#include <math.h>
#include <algorithm>
#define DEBUG 0


#include <stdio.h>            /* C input/output                       */
#include <stdlib.h>           /* C standard library                   */
#include <glpk.h>             /* GNU GLPK linear/mixed integer solver */

/// The format of a given file.
///
enum filetype {
  MPS = 0,  ///< Given file is in the MPS format
  LP = 1    ///< Given file is in the LP format   
};
/// Flags, which indicate the different bounds to be calculated for given LP.
/// For instance if UPPER is set the function getMatrix() will calculate the upper bounds for the specified LP object.
enum bounds {
    UPPER=GLP_UP, ///< Upper bounds
    LOWER=GLP_LO, ///< Lower bounds
    EQUAL=GLP_FX, ///< Fixed bounds
    UNBOUND=GLP_FR///< Unbounded
}; // ax < b, ax > b, ax = b, ax < 0

/// Flags used for distinguishing between the different scaling types to be used by the defined functions.
///
enum scaling {
    GEOMMEAN=GLP_SF_GM, ///< Geometric mean scaling
    EQUILIB=GLP_SF_EQ   ///< Equilibration scaling
};

///@brief Opens a specified LP by calling the constructor of the GLPK solver.
///@param fname The name of the file to be opened
///@param format The filetype of given file either MPS or LP are valid (see enum filetype)
///
void openLP(const std::string & fname, int format);

///@brief Closes the given LP by deallocating memory
///
///
///
void closeLP(void);

///@brief Calculates properties of a given LP depending on the bounds Flag
///@param boundquery A Flag, which indicates which matrix is going to be calculated
///@param scaled An integer, which indicates a scaled matrix(LP)
///@return A Vector (structure) equivalent to a matrix with 4 rows
std::vector<double> getMatrix(bounds boundquery, int scaled);

///@brief Calculates the objective of a given LP
///@param scaled An integer, which indicates a scaled matrix(LP)
///@return The objective of a given LP as vector
///
std::vector<double> getObjective(int scaled);

///@brief Does scaling for the given LP
///@param sctype A Flag, which indicates which scaling type is to be used by the called function.
///
void doScaling(scaling sctype);

///@brief Solves the given LP with an off-the-shelf LP-Solver for instance using the Gnu glpk
///
///
///
void solve();


