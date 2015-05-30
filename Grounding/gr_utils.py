from __future__ import print_function
import pulp

class Math_prob:
    def __init__(self):
        self.num_vars = 0
        self.num_cons_linear = 0
        self.num_cons_nonlinear = 0
        self.vars = dict()
        self.cons_linear = dict()
        self.objective = dict()
        self.solutions = dict()
    
    def add_var(self, lower=0, upper=1):
        self.vars[self.num_vars] = (lower, upper)
        self.num_vars += 1
        return self.num_vars - 1
    
    def get_vars(self):
        variables = [(var_id, self.vars[var_id][0], self.vars[var_id][1]) for var_id in self.vars]
        return variables
     
    def get_objective(self):
        objective = [(var_id, self.objective[var_id]) for var_id in self.objective]
        return objective
    
    def get_linear_cons(self):
        conss = [self.cons_linear[i] for i in self.cons_linear]
        return conss
    
    def get_solutions(self):
        return self.solutions
        
    def add_linear_constraint(self, var_indices, var_coefs, constant):
        self.cons_linear[self.num_cons_linear] = (var_indices, var_coefs, constant)
        self.num_cons_linear += 1
        return self.num_cons_linear - 1
    
    def add_to_objective(self, entity, weight):
        if not entity[0]:
            if entity[1] in self.objective:
                self.objective[entity[1]] += weight
            else:
                self.objective[entity[1]] = weight
    
    def print_cons_linear(self):
        for cons in self.cons_linear:
            print ('%d:\t' %(cons), end='')
            v, co, c = self.cons_linear[cons]
            for i in range(len(v)):
                if co[i] >= 0:
                    if i > 0:
                        print(' + ',end='')
                else:
                    print(' - ',end='')
                if abs(co[i]) != 1 :
                    print(abs(co[i]),end='') 
                print(' x_%d' %(v[i]),end='')
            if c != 0:
                if c > 0:
                    print(' + ',end='')
                else:
                    print(' - ',end='')
                print ('%f' %abs(c),end='')
            print(' <= 0')
            
    def print_objective(self):
        first = True
        for v in self.objective:
            c = self.objective[v]
            if not first:
                print (' + ',end='')
            else:
                first = False
            if c != 1:
                print('%.3f ' %c,end='')
            print('x_%d' %v,end='')
        print()
        
    def pulp_solve(self):
        problem = pulp.LpProblem(pulp.LpMinimize)

        vs = self.get_vars()
        our_vars = dict()
        v = []
        for i in range(len(vs)):
            v.append(pulp.LpVariable('%d' %vs[i][0], vs[i][1], vs[i][2]))
            our_vars[vs[i][0]] = v[i]

        ob = self.get_objective()
        problem.objective = pulp.LpAffineExpression([(our_vars[ob[i][0]], ob[i][1]) for i in range(len(ob))])

        css = self.get_linear_cons()
        for i in range(len(css)):
            ids, coefs, cnst = css[i]
            c = pulp.LpConstraint(
                pulp.LpAffineExpression([(our_vars[ids[j]], coefs[j]) for j in range(len(coefs))], 
                                        constant=cnst)
                , sense=-1)
            problem.constraints[i] = c
            
        problem.solve()
        self.solutions.clear()
        for variable in problem.variables():
            self.solutions[int(variable.name)] = variable.varValue
