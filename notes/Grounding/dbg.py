#!/usr/bin/env python

from gr_utils import Math_prob

def psl_and(problem, left, right, l_negated=False, r_negated=False):
    m, n = (left[1], right[1])
    m_coef, n_coef = (1,1)
    cons = 0
    
    if l_negated:
        if left[0]:
            m = 1-m
        else:
            m_coef = -1
            cons += 1
    
    if r_negated:
        if right[0]:
            n = 1-n
        else:
            n_coef = -1
            cons += 1
        
    if left[0] and right[0]:
        return (True, max(0, m+n-1))
    elif not left[0] and not right[0]:
        y = problem.add_var()
        problem.add_linear_constraint([m,n,y], [m_coef,n_coef,-1], (cons-1))
        return (False, y)
    elif not left[0] and right[0]:
        y = problem.add_var()
        problem.add_linear_constraint([m,y], [m_coef,-1], cons+n-1)
        return (False, y)
    elif left[0] and not right[0]:
        y = problem.add_var()
        problem.add_linear_constraint([n,y], [n_coef,-1], cons+m-1)
        return (False, y)
    

def psl_or(problem, left, right, l_negated=False, r_negated=False):
    m, n = (left[1], right[1])
    m_coef, n_coef = (-1,-1)
    cons = 0
    
    if l_negated:
        if left[0]:
            m = 1-m
        else:
            m_coef = 1
            cons -= 1
    
    if r_negated:
        if right[0]:
            n = 1-n
        else:
            n_coef = 1
            cons -= 1
        
    if left[0] and right[0]:
        return (True, max(0, m+n-1))
    elif not left[0] and not right[0]:
        y = problem.add_var()
        problem.add_linear_constraint([m,n,y], [m_coef,n_coef,1], cons)
        return (False, y)
    elif not left[0] and right[0]:
        y = problem.add_var()
        problem.add_linear_constraint([m,y], [m_coef,1], cons+n-1)
        return (False, y)
    elif left[0] and not right[0]:
        y = problem.add_var()
        problem.add_linear_constraint([n,y], [n_coef,1], cons+m-1)
        return (False, y)


people_rel = dict()
with open('./people.csv') as people_file:
    people_file.readline()
    for line in people_file:
        line = line.strip().split(',')
        current_tuple = [int(line[0]), line[1]]
        people_rel[current_tuple[0]] = current_tuple[1]

# for key in people_rel.keys()[:5]:
#     print('%d %s' %(key, people_rel[key]))

knows_rel = dict()
with open('./knows.csv') as knows_file:
    knows_file.readline()
    for line in knows_file:
        line = line.strip().split(',')
        current_tuple = [int(line[0]), int(line[1]), float(line[2])]
        knows_rel[(current_tuple[0], current_tuple[1])] = (True, current_tuple[2])
        
opt_prob = Math_prob()
for person1 in people_rel:
    for person2 in people_rel:
        current_tuple = (person1, person2)
        if not current_tuple in knows_rel:
            knows_rel[current_tuple] = (False, opt_prob.add_var())

# for key in knows_rel.keys()[:5]:
#     print(key, knows_rel[key])

trusts_rel = dict()
with open('./trusts.csv') as knows_file:
    knows_file.readline()
    for line in knows_file:
        line = line.strip().split(',')
        current_tuple = [int(line[0]), int(line[1]), float(line[2])]
        trusts_rel[(current_tuple[0], current_tuple[1])] = (True, current_tuple[2])
for person1 in people_rel:
    for person2 in people_rel:
        current_tuple = (person1, person2)
        if not current_tuple in trusts_rel:
            trusts_rel[current_tuple] = (False, opt_prob.add_var())

# for key in trusts_rel.keys()[:5]:
#     print(key, knows_rel[key])

ground_rules = [(knows_rel[(person1, person2)],
                 knows_rel[(person2, person1)],
                 trusts_rel[(person2, person1)],
                 trusts_rel[(person1, person2)])
                for person1 in people_rel for person2 in people_rel]

weight1 = 1
for F1, F2, F3, F4 in ground_rules:
    M1 = psl_and(opt_prob, F1, F2)
    M2 = psl_and(opt_prob, M1, F3, r_negated=True)
    Dist = psl_and(opt_prob, M2, F4)
    opt_prob.add_to_objective(Dist, weight1)


#opt_prob.print_objective()
opt_prob.pulp_solve()
#opt_prob.print_cons_linear()
#print(opt_prob.get_linear_cons())
print(opt_prob.solutions)
