import string
import itertools as it
from pyDatalog import pyDatalog

# --------------------------------------------------------------------
# create lots of variable names for convenience.
# A-Z, A1-A9 ... Z1-Z9

for s in string.uppercase[:26]:
  pyDatalog.create_terms(s)
  for n in range(1,9):
    pyDatalog.create_terms(s+str(n))
# --------------------------------------------------------------------


# LogKB Fact management

def loadFacts(fileName):
  """
  Convenience function to open a fact file and load it into the LogKB.
  """
  facts = open(fileName)
  pyDatalog.load(facts.read())
  facts.close()


def retractAll(pname, arity):
  """
  retract all facts of given predicate name and arity from the LogKB.
  """
  vnames  = ["V" + str(x) for x in range(0,arity)]
  varlist = "(" + ",".join(vnames) + ")"
  query = pname + varlist
  ans = pyDatalog.ask(query)
  for r in ans.answers:
    pyDatalog.retract_fact(pname,*list(r))

def assertAll(pname, facts):
  """
  Assert all tuples in facts into the LogKB, using predicate name pname.
  Expects a list of tuples in facts.
  """
  for f in facts: 
    pyDatalog.assert_fact(pname, *f)


# Python predicate implementations

# Predicates may be used to resolve information in different ways, with different parameters
# known and constant (C)  or not known and to resolve (V). For a rigid implementation it
# is necessary to have implementations for all possible cases. In the implementation below,
# some cases are left out as they were not needed. If a predicate is used in such a constellation,
# an exception is thrown instead, signalling the case which would have to be implemented for the
# resp. predicate.


# combinatorial functions and findall emulation

pyDatalog.create_terms('combinations, combReplace, findall, rotations')

@pyDatalog.predicate()
def combinations3(N,L1,L2):
  """
  k-combinations of length N
  use cases: combinations(C,C,V) -> resolve k-combinations of L1 to L2
             combinations(C,C,C) -> assert that L2 is a k-combination of L1.
  """
  if (N.is_const() and L1.is_const() and not L2.is_const()):
    result = it.combinations(L1.id,N.id)
    for x in result:
      yield (N,L1,x)
  elif (N.is_const() and L1.is_const() and L2.is_const()):
    if (len(L2.id) == N.id and tupleIsSubseq(L2.id,L1.id)):
      yield (N,L1,L2)
  else:
    raise Exception("unhandled case in combinations: {0},{1},{2}".format(N.is_const(),L1.is_const(),L2.is_const()))


def combReplace3(N,L1,L2):
  """
  combinations with replacement of length N
  use cases: combinations(C,C,V) -> resolve combinations of L1 to L2
  """
  if (N.is_const() and L1.is_const() and not L2.is_const()):
    result = it.combinations_with_replacement(L1.id,N.id)
    for x in result:
      yield (N,L1,x)
  else:
    raise Exception("unhandled case in combReplace: {0},{1},{2}".format(N.is_const(),L1.is_const(),L2.is_const()))

@pyDatalog.predicate()
def rotations2(L,L1):
  """
  list rotation
  use cases: rotations(C,V) -> resolve rotations of L1 to L2
  """
  if (L.is_const() and not L1.is_const()):
    v = list(L.id)
    for i in range(0,len(v)):
      k = tuple(v)
      v.append(v.pop(0))
      yield (L,k)
  else:
    raise Exception("unhandled case in rotations: {0},{1}".format(L.is_const(),L1.is_const()))


@pyDatalog.predicate()
def findall2(S,L):
  """
  Hackish PROLOG findall emulation.
  use cases: findall(C,V) -> Given a query String in S, ask the LogKB and resolve to a list of results in L.
  """
  if (S.is_const() and not L.is_const()):
    result = pyDatalog.ask(S.id).answers
    result.sort()
    yield (S,tuple(result))
  else:
    raise Exception("unhandled case in findall: {0},{1}".format(S.is_const(),L.is_const()))


# cons list implementation
# As pyDatalog allows tuples in the syntax and handles them as atoms, it it possible to 
# implement list-valued atoms in the form of cons lists.
#
# Most of the list functions below can also be directly implemented as datalog statements,
# however doing that is terribly slow. To speed things up, here are Python implementations.


pyDatalog.create_terms('nil,length,singleton,cons,member,pair,concat,intersection,union,X')

# the empty tuple is the empty list
nil(X) <= (X == ())

@pyDatalog.predicate()
def length2(L,X):
  """
  Calculate the length of a list.
  use cases: length(C,V) -> resolve the length of L in X
  """
  if (X.is_const() and not L.is_const()):
    yield (len(X.id),X)
  else:
    raise Exception("unhandled case in length: {0},{1}".format(L.is_const(),X.is_const()))

@pyDatalog.predicate()
def singleton2(X,L):
  """
  Create a list with exactly one element
  use cases: singleton(C,V) -> create a list in L containing X as singleton element.
  """
  if (X.is_const()) and not L.is_const():
    yield (X,(X.id,))
  else:
    raise Exception("unhandled case in singleton: {0},{1}".format(X.is_const(),L.is_const()))

@pyDatalog.predicate()
def cons3(H,T,L):
  """
  List construction and deconstruction. Represent a list L as head H and tail T.
  use cases: cons(V,V,C) -> deconstruct L into H and T
             cons(C,C,V) -> construct L from given H and T
             cons(C,C,C) -> satisfiable if L can be deconstructed into given H and T.
  """
  if (L.is_const() and not H.is_const() and not T.is_const()):
    if (len(L.id) > 0):
      yield (L.id[0],L.id[1:],L)
  elif (H.is_const() and T.is_const() and not L.is_const()):
    yield (H,T,(H.id,) + T.id)
  elif (H.is_const() and T.is_const() and L.is_const()):
    if (((H.id,) + T.id) == L.id):
      yield (H,T,L)
  else:
    raise Exception("unhandled case in cons: {0},{1},{2}".format(H.is_const(),T.is_const(),L.is_const()))

@pyDatalog.predicate()
def member2(X,L):
  """
  Test list membership.
  use cases: member(C,C) -> satisfiable if X is element of L.
  """
  if (X.is_const() and L.is_const()):
    if (X.id in L.id):
      yield (X,L)
  else:
    raise Exception("unhandled case in member: {0},{1}".format(X.is_const(),L.is_const()))

@pyDatalog.predicate()
def concat3(L1,L2,C):
  """
  List concatenation.
  use cases: concat(C,C,V) -> construct C by concatenating L1 and L2.
  """
  if (L1.is_const() and L2.is_const() and not C.is_const()):
    yield (L1,L2,L1.id + L2.id)
  else:
    raise Exception("unhandled case in concat: {0},{1},{2}".format(L1.is_const(),L2.is_const(),C.is_const()))

@pyDatalog.predicate()
def intersection3(L1,L2,I):
  """
  Set-like list intersection.
  use cases: intersection(C,C,V) -> resolve I to the list of elements both contained in L1 and L2.
  Warning! This implementation is not commutative.
  """
  if (L1.is_const() and L2.is_const() and not I.is_const()):
    result = tupleIntersection(L1.id,L2.id)
    yield (L1,L2,result)
  else:
    raise Exception("unhandled case in intersection: {0},{1},{2}".format(L1.is_const(),L2.is_const(),I.is_const()))

@pyDatalog.predicate()
def union3(L1,L2,U):
  """
  Set-like list union.
  use cases: union(C,C,V) -> resolve I to the concatenation of L1 and the elements of L2, which are not in L1.
  Warning! This implementation is not commutative.
  """
  if (L1.is_const() and L2.is_const() and not U.is_const()):
    result = tupleUnion(L1.id,L2.id)
    yield (L1,L2,result)
  else:
    raise Exception("unhandled case in union: {0},{1},{2}".format(L1.is_const(),L2.is_const(),U.is_const()))

@pyDatalog.predicate()
def pair3(X,Y,P):
  """
  Pair construction/deconstruction. A pair is a list with two elements.
  use cases: pair(C,C,V) -> construct P as (X,Y).
             pair(V,V,C) -> deconstruct P into X and Y.
  """
  if (X.is_const() and Y.is_const() and not P.is_const()):
    yield (X,Y,(X.id, Y.id))
  elif (P.is_const() and not X.is_const and not Y.is_const()):
    yield (P.id[0],P.id[1],P)
  else:
    raise Exception("unhandled case in pair: {0},{1},{2}".format(X.is_const(),Y.is_const(),P.is_const()))


def tupleIntersection(a,b):
  """
  Return all elements x which are both in a and b. noncommutative. order dependent.
  """
  return tuple([x for x in a if x in b])

def tupleUnion(a,b):
  """
  Return tuple containing a and all elements of b which are not in a. noncommutative. order dependent.
  """
  return a + tuple([x for x in b if x not in a])

def tupleIsSubseq(a,b):
  """
  True if a is a subsequence of b.
  """
  return tupleIntersection(b,a) == a
