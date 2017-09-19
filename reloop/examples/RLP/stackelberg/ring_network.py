from pyDatalogUtil import *

# A pyDatalog model for a ring network

# expected predicates
# edge/2
#   src : REF
#   dst : REF

# resources/1
#   amt : INT


pyDatalog.create_terms("node,edge,resources,adjacent,path,edgeList,endpoint,stPair,stPath,degree,innerEdge,edgeSet,degreeSum,pathLength")
pyDatalog.create_terms("leaderAction,followerAction,interactions,gameMatrix,followerOccurrence,leaderUtility,followerUtility")

# Undirected representation. Two nodes X,Y are adjacent if there is an edge X->Y or an edge Y->X
adjacent(X,Y) <= edge(X,Y)
adjacent(X,Y) <= edge(Y,X)

# A node X is something which is adjacent to something else (Y).
node(X) <= adjacent(X,Y)

# The degree of a node Y is the sum (len_) of neighboring nodes.
# Thus it is also the number of adjacent edges.
# (len aggregate: pyDatalog builtin evaluating to size of the result set of the RHS of <= )
(degree[Y] == len_(X)) <= node(X) & node(Y) & adjacent(X,Y)

# An endpoint X is a node with a degree of 1
endpoint(X) <= node(X) & (degree[X] == 1)

# An inner edge between nodes X and Y is an edge where both nodes are not endpoints.
# Yes, we really need the undirected edge info here, because this will later be used to
# construct the blocking sets where we refer to the original edges in the graph definition.
innerEdge(X,Y) <= edge(X,Y) & ~endpoint(X) & ~endpoint(Y)

# A s-t pair (source-sink pair) is a pair of nodes such that both are endpoints and both are separate nodes.
stPair(X,Y) <= endpoint(X) & endpoint(Y) & (X != Y)

# Node path declaration, base case
#
# A path between X and Y exists if these objects are adjacent.
# in this case the Path P will be the cons-list (X,Y)
path(X,Y,P) <= adjacent(X,Y) & (P == (X,Y))

# Node path declaration, recursive case
#
# A path between two nodes X and Y exists if there is a node Z such that X is adjacent to Z.
# and there exists a path P2 between Z and Y such that X is not a member of P2, i.e. the path is loop-free.
# Then the resultant path P is the extension of P2 with the node X and P is given as a cons-list.
path(X,Y,P) <= node(X) & node(Y) & node(Z) & adjacent(X,Z) & path(Z,Y,P2) & ~member(X,P2) & cons(X,P2,P)

# Edge path declaration, base case
#
# The edge list for a path X which has length 1 (only a single node) is the empty list.
edgeList(X,()) <= length(L,X) & (L == 1)

# Edge path declaration, recursive case 1
#
# If elements X and Y are the two leading elements in the node path P
# and there is an edge between X and Y
# and an edge path L1 starting in Y can be inferred
# then the edge list L is extended by the edge (X,Y)
edgeList(P,L)  <= cons(X,T1,P) & cons(Y,T2,T1) & edgeList(T1,L1) & edge(X,Y) & pair(X,Y,E) & cons(E,L1,L)

# Edge path declaration, recursive case 2
#
# If elements X and Y are the two leading elements in the node path P
# and there is an edge between Y and X
# and an edge path L1 starting in Y can be inferred
# then the edge list L is extended by the edge (Y,X)
edgeList(P,L)  <= cons(X,T1,P) & cons(Y,T2,T1) & edgeList(T1,L1) & edge(Y,X) & pair(Y,X,E) & cons(E,L1,L)

# A s-t path exists if there is a path between nodes X,Y of a s-t pair.
stPath(X,Y,P) <= stPair(X,Y) & path(X,Y,P)

# An edge set of size K is constructed
# by first enumerating all inner edges into a list X (via a hackish PROLOG findall emulation)
# And then resolving all K-combinations of X into the resultant list E.
# (implementations in pyDatalogUtil)
edgeSet(K,E) <= findall("innerEdge(X,Y)",X) & combinations(K,X,E)

# The "sum of degrees" preference relation is 0 for the empty list.
+degreeSum((),0.0)
# Otherwise it is the sum of the degree of the head of the list X
# plus the sum of degrees of the tail of the list T.
# As degree/1 is resolvable only for node/1 instances, we do not need
# to say node(X) here explicitly, but we could.
degreeSum(P,N)  <= cons(X,T,P) & degreeSum(T,N1)  & (N == N1 + degree[X])

# The interaction of a follower and a leader action is defined by the intersection of
# the leaders blocking set with the followers edge path.
interactions(E,P,I) <= followerAction(P) & leaderAction(E) & edgeList(P,L) & intersection(L,E,I)

# The game matrix defines a zero sum game.
# V1 is the payoff for the leader, V2 is the payoff for the follower.
# The follower wins the play if the interaction between leader action L and follower action F is empty,
# i.e. the leader does not block the follower path.
gameMatrix(L,F,V1,V2) <= interactions(L,F,I) & nil(I) & degreeSum(F,V) & (V1 == -V) & (V2 == V)
# The leader wins the play if the interaction between leader action L and follower action F is nonempty,
# i.e. the leader blocks the follower path.
gameMatrix(L,F,V1,V2) <= interactions(L,F,I) & ~nil(I) & degreeSum(F,V) & (V1 == V) & (V2 == -V)

# As DOBSS wants to have separate leader and follower utilities we need to map some predicates of the
# model to predicates interpretable by DOBBS.

# A leader action is an edge set of size R.
leaderAction(E) <= resources(R) & edgeSet(R,E) 
# The leader utility is the projection of L,F,V1 of the game matrix. As there is only one follower,
# the follower type "f1" is hardcoded.
leaderUtility("f1",L,F,V1) <= gameMatrix(L,F,V1,V2)

# The follower "f1" occurs with 100% probability.
+followerOccurrence("f1",1.0)
# A follower action P is any s-t path inferred through the model.
followerAction(P) <= stPath(X,Y,P)
# The follower utility is the projection of L,F,V2 of the game matrix. As there is only one follower,
# the follower type "f1" is hardcoded.
followerUtility("f1",L,F,V2) <= gameMatrix(L,F,V1,V2)
