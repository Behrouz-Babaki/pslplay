#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

d1 = dict()
d2 = dict()

with open('./knows_infer.csv') as f:
    for line in f:
        line = line.strip().split(',')
        [p1, p2] = line[:2]
        val = float(line[-1])
        d1[(p1, p2)] = val   
        
with open('/home/behrouz/temp/test_psl_cli/output/KNOWS.csv') as f:
    for line in f:
        line = line.strip().split(',')
        [p1, p2] = line[:2]
        val = float(line[-1])
        d2[(p1, p2)] = val         
        
with open('/home/behrouz/temp/psl-examples/link_prediction/easy/groovy/output/default/knows_infer2.txt') as f:
    line = f.readline().strip()
    assert(line == '--- Atoms:')
    line = f.readline().strip()
    while not line.startswith('# Atoms: '):
        m = re.match(r"KNOWS\(('\w+'), ('\w+')\) Truth=\[([\d\.]+)\]", line)
        d2[m.group(1), m.group(2)] = float(m.group(3))
        line = f.readline().strip()
        
for pair in d2:
    if d1[pair]!=d2[pair]:
        print(pair, d1[pair], d2[pair])