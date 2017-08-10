#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from gr_core import Math_prob, add_rule
from gr_utils import read_link_data, write_link_mpe

opt_prob = Math_prob()

(knows_rel, likes_rel,
lived_rel, people,
interests, places) = read_link_data('./data/knows_obs.txt',
                                           './data/knows_targets.txt',
                                           './data/likes_obs.txt',
                                           './data/lived_obs.txt',
                                           opt_prob)

# 20:  Lived(P1,L) & Lived(P2,L) & P1!=P2   -> Knows(P1,P2)
ground_rules = [(lived_rel[(A, C)],
                 lived_rel[(B, C)],
                 (True, float(A!=B)),
                 knows_rel[(A, B)])
                for A in people
                for B in people
                for C in places
                if A!=B]
signs = [False, False, False, False]
weight = 20.0
counter = add_rule(ground_rules, signs, weight, opt_prob)
print(counter)

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
weight = 5.0
counter = add_rule(ground_rules, signs, weight, opt_prob)
print(counter)

# 10:  Likes(P1,L) & Likes(P2,L) & P1!=P2  -> Knows(P1,P2)
ground_rules = [(likes_rel[(A, C)],
                 likes_rel[(B, C)],
                 (True, float(A!=B)),
                 knows_rel[(A, B)])
                for A in people
                for B in people
                for C in interests
                if A!=B
                ]
signs = [False, False, False, False]
weight = 10.0
counter = add_rule(ground_rules, signs, weight, opt_prob)
print(counter)

# 5:   Knows(P1,P2) & Knows(P2,P3) & P1!=P3 -> Knows(P1,P3)
ground_rules = [(knows_rel[(A, B)],
                 knows_rel[(B, C)],
                 (True, float(A!=C)),
                 knows_rel[(A, C)])
                for A in people
                for B in people
                for C in people
                if (A!=B and B!=C and A!=C)]

signs = [False, False, False, False]
weight = 5.0
counter = add_rule(ground_rules, signs, weight, opt_prob)
print(counter)


# 10000: Knows(P1,P2) -> Knows(P2,P1)
ground_rules = [(knows_rel[(A, B)],
                 knows_rel[(B, A)])
                for A in people
                for B in people
                if A!=B]

signs = [False, False]
weight = 10000.0
counter = add_rule(ground_rules, signs, weight, opt_prob)
print(counter)

# 5:  !Knows(P1,P2)
ground_rules = [(knows_rel[(A, B)],)
                for A in people
                for B in people
                if A!=B]

signs = [True]
weight = 5.0
counter = add_rule(ground_rules, signs, weight, opt_prob)
print(counter)

opt_prob.pulp_solve()
write_link_mpe('./knows_infer.csv', people, knows_rel, opt_prob)
