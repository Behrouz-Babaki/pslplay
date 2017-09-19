import itertools as it
from reloop.solvers.lpsolver import *
from pyDatalogUtil import *

# DOBSS
# Two implementations of the DOBSS algorithm as linear program,
# based on "Efficient Algorithms to solve Stackelberg Security Games"
# by Paruchuri et al. (AAAI 2008)

# The LP model expects the following predicates to be resolvable by the LogKB

#   leaderAction/1 
#      ID : actionName
#
#   leaderUtility/4
#      REF : followerType
#      REF : leaderAction
#      REF : followerAction
#      VAL : utilityValue
#
#   followerAction/1
#      ID  : actionName
#
#   followerOccurrence/2
#      ID  : followerName
#      VAL : occurrenceProbability
#
#   followerUtility/4
#      REF : followerType
#      REF : leaderAction
#      REF : followerAction
#      VAL : utilityValue

pyDatalog.create_terms("leaderAction,leaderUtility,followerType,followerAction,followerOccurrence,followerUtility")

# Define follower types based on follower occurrences, to keep these two predicates
# consistent with each other
followerType(T) <= followerOccurrence(T,X)

def rotations(n):
  """
  calculate all possible rotations of a list of length n in which exactly one
  element is set to 1 and all other elements are set to 0.
  """
  v = [1] + [0] * (n-1)
  for i in range(0,n):
    k = list(v)
    v.append(v.pop(0))
    yield k

#
# DOBSS SUBPROBLEM LP
#

def enumStates(fTypes, fActions):
  """
  Given a set of follower types fTypes and a set of follower actions, compute a list of states
  of the integer variable, such that one element in the list can be later asserted as a set of
  facts in the LogKB.
  """
  n = len(fActions)
  m = len(fTypes)
  # label a "selected action" vector given by rotations(n) with the respective action name.
  a = [zip(fActions,r) for r in rotations(n)]

  # calculate the product over followerTypes for the action selections.
  for s in it.combinations_with_replacement(a,m):
    # label s by follower types and deconstruct it into lists of assertable facts. yield one list per state.
    yield [(t,x,y) for t,k in zip(fTypes,s) for x,y in k]


def solve_dobss_subproblems(grounderClass, logkb, solverClass):
  """
  Instantiate a RLP model and solve it with given grounder logkb and solver, using the sequential LP method derived
  from state enumeration with the DOBSS MIQP.
  """
  
  # DATALOG: ask followerType(X), ask followerAction(Y)
  followerType(X)
  followerAction(Y)
  
  # calculate state enumeration
  ivarStates = enumStates(X.data,Y.data)

  # data binding
  leader_action = boolean_predicate("leaderAction",1)
  leader_util   = numeric_predicate("leaderUtility",3)
  
  follower_type       = boolean_predicate("followerType",1)
  follower_action     = boolean_predicate("followerAction",1)
  follower_state      = numeric_predicate("ivarState",2)
  follower_occurrence = numeric_predicate("followerOccurrence",1)
  follower_util       = numeric_predicate("followerUtility",3)

  leader_strategy = numeric_predicate("leaderStrategy",1)
  slack           = numeric_predicate("slack",1)

  M = 1000

  # main iteration over all possible states
  for state in ivarStates:
    # temporarily assert the current state to the LogKB
    assertAll("ivarState",state)

    # initialize and build RLP model
    grounder = grounderClass(logkb)
    model = RlpProblem("Stackelberg-DOBSS", LpMaximize, grounder, solverClass)
    model.add_reloop_variable(leader_strategy)
    model.add_reloop_variable(slack)

    I, J, L = sub_symbols('I', 'J', 'L')

    model += RlpSum([L,I,J], leader_action(I) & follower_type(L) & follower_action(J),
	          follower_occurrence(L) 
	          * leader_util(L,I,J)
	          * follower_state(L,J)
	          * leader_strategy(I)
	        )


    model += RlpSum([I,], leader_action(I), leader_strategy(I)) |eq| 1.0
  
    model += ForAll([I,], leader_action(I), leader_strategy(I) |ge| 0.0)

  
    model += ForAll([L,J], follower_type(L) & follower_action(J),
		    RlpSum([I,], leader_action(I),follower_util(L,I,J) * leader_strategy(I)) |le| slack(L)) 

    model += ForAll([L,J], follower_type(L) & follower_action(J),
		    slack(L) - RlpSum([I,], leader_action(I),follower_util(L,I,J) * leader_strategy(I))
		    |le| (1 - follower_state(L,J)) * M
		    )
    model.solve()
    
    # retract the current state
    retractAll("ivarState",3)

#
# DOBSS BLOCK LP
#


def enumIvarStates1(fTypes, fActions):
  """
  Given a set of follower types fTypes and a set of follower actions, compute a list of states
  of the integer variable, such that one element in the list can be later asserted as a set of
  facts in the LogKB.
  
  yield assertable facts such that the facts for each state are labeled with the same state number i.
  """
  n = len(fActions)
  m = len(fTypes)
  a = [zip(fActions,r) for r in rotations(n)]
  c = it.combinations_with_replacement(a,m)
    
  i = 0
  for s in c:
    i = i + 1
    for t,k in zip(fTypes,s):
      for x,y in k:
	yield (i,t,x,y) 

def enumSpStates(ivarStates):
    """
    Extract the state numbers i, so they can be asserted and used as an index
    In hindsight this could have also been a pure logical statement.
    """
    c = -1
    for (i,t,x,y,) in ivarStates:
      if (i != c):
	c = i
	yield (i,)

def solve_dobss_block(grounderClass, logkb, solverClass):
  """
  Instantiate a RLP model and solve it with given grounder logkb and solver, using the block LP method.
  """
  
  # DATALOG : ask followerType(X), ask followerAction(Y)
  followerType(X)
  followerAction(Y)
  
  # generate state space ivarStates
  ivarStates = list(enumIvarStates1(X.data,Y.data))
  # generate state number index spStates
  spStates   = list(enumSpStates(ivarStates))

  # data binding
  leader_action = boolean_predicate("leaderAction",1)
  leader_util   = numeric_predicate("leaderUtility",3)

  sp_state            = boolean_predicate("spState",1)  
  follower_type       = boolean_predicate("followerType",1)
  follower_action     = boolean_predicate("followerAction",1)
  follower_state      = numeric_predicate("ivarState",3)
  follower_occurrence = numeric_predicate("followerOccurrence",1)
  follower_util       = numeric_predicate("followerUtility",3)

  leader_strategy = numeric_predicate("leaderStrategy",2)
  slack           = numeric_predicate("slack",2)

  M = 1000

  # assert the whole state space at once
  assertAll("ivarState", list(ivarStates))
  assertAll("spState", list(spStates))

  # build and instantiate model
  grounder = grounderClass(logkb)
  model = RlpProblem("Stackelberg-DOBSS", LpMaximize, grounder, solverClass)
  model.add_reloop_variable(leader_strategy)
  model.add_reloop_variable(slack)

  S, I, J, L = sub_symbols('S', 'I', 'J', 'L')

  # Instead of enumerating each state in a for loop we have extended the query of the supporting set
  # by an additonal logical variable S which resolves to the current state number
  # the follower_state and leader_strategy predicates have been extended by S, which leads to
  # decision variable replication and a separate block of constraints for each copy of the 
  # decision variables.
  model += RlpSum([S,L,I,J], sp_state(S) & leader_action(I) & follower_type(L) & follower_action(J),
		  follower_occurrence(L) 
	          * leader_util(L,I,J)
	          * follower_state(S,L,J)
	          * leader_strategy(S,I)
	        )


  model += ForAll([S], sp_state(S),  RlpSum([I,], leader_action(I), leader_strategy(S,I)) |eq| 1.0)
  
  model += ForAll([S,I], sp_state(S) & leader_action(I), leader_strategy(S,I) |ge| 0.0)

  
  model += ForAll([S,L,J], sp_state(S) & follower_type(L) & follower_action(J),
		    RlpSum([I,], leader_action(I),follower_util(L,I,J) * leader_strategy(S,I)) |le| slack(S,L)) 

  model += ForAll([S,L,J], sp_state(S) & follower_type(L) & follower_action(J),
		    slack(S,L) - RlpSum([I,], leader_action(I),follower_util(L,I,J) * leader_strategy(S,I))
		    |le| (1 - follower_state(S,L,J)) * M
		    )
  model.solve()
  
  # retract the whole state space
  retractAll("ivarState",4)
  retractAll("spState",1)
