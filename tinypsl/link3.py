#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from gr_core import Math_prob, check_rule
from gr_utils import read_link_data, write_link_mpe

opt_prob = Math_prob()

(knows_rel, likes_rel,
lived_rel, people,
interests, places) = read_link_data('./data/knows_obs.txt',
                                           './data/knows_targets.txt',
                                           './data/likes_obs.txt',
                                           './data/lived_obs.txt',
                                           opt_prob)

# 5:  Lived(P1,L1) & Lived(P2,L2) & P1!=P2 & L1!=L2  -> !Knows(P1,P2)
ground_rules = [(lived_rel[(A, C)],
                 lived_rel[(B, D)],
                 (True, float(A!=B)),
                 (True, float(C!=D)),
                 knows_rel[(A, B)])
                for A in people
                for B in people
                for C in places
                for D in places
                if A!=B
                ]
signs = [False, False, False, False, True]
for A in people:
    for B in people:
        if A!=B:
            for C in places:
                for D in places:
                    g = (lived_rel[(A, C)], lived_rel[(B, D)],
                        (True, float(A!=B)), (True, float(C!=D)),
                         knows_rel[(A, B)])
                    if check_rule(g, signs): 
                        f = dict(P1=people[A], P2=people[B], 
                                 L1=places[C], L2=places[D])
                        print("5.0:(~(KNOWS('{P1}','{P2}')) | ~(('{L1}' != '{L2}')) | ~(LIVED('{P2}', '{L2}')) | ~(('{P1}' != '{P2}')) | ~(LIVED('{P1}', '{L1}')))".format(**f))
