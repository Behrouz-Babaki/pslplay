from pyDatalogUtil import *

# expected predicates
# activeScenario/1

pyDatalog.create_terms("scenario,gameMatrix,leaderAction,followerAction,followerOccurrence,activeScenario,leaderUtility,followerUtility")

+leaderAction("la1")
+leaderAction("la2")
+leaderAction("la3")

+followerAction("fa1")
+followerAction("fa2")
+followerAction("fa3")

+followerOccurrence("f1",1.0)

leaderUtility("f1",X,Y,V) <= ( scenario(Q)
			     & activeScenario(Q)
			     & gameMatrix(Q,X,Y,V,W)
			     )

followerUtility("f1",X,Y,W) <= ( scenario(Q)
			       & activeScenario(Q)
			       & gameMatrix(Q,X,Y,V,W)
			       )


