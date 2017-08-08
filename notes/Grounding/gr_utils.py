from __future__ import print_function

def read_trust_data(p_fname, k_fname, t_fname, problem, separator=',', drop_header=True):
    people_rel = dict()
    with open(p_fname) as people_file:
	if drop_header:
	        people_file.readline()
        for line in people_file:
            line = line.strip().split(separator)
            current_tuple = [int(line[0]), line[1]]
            people_rel[current_tuple[0]] = current_tuple[1]
            
    knows_rel = dict()
    with open(k_fname) as knows_file:
	if drop_header:
	        knows_file.readline()
        for line in knows_file:
            line = line.strip().split(separator)
            current_tuple = [int(line[0]), int(line[1]), float(line[2])]
            knows_rel[(current_tuple[0], current_tuple[1])] = (True, current_tuple[2])
            
    for person1 in people_rel:
        for person2 in people_rel:
            current_tuple = (person1, person2)
            if not current_tuple in knows_rel:
                knows_rel[current_tuple] = (False, problem.add_var())
                
    trusts_rel = dict()
    with open(t_fname) as knows_file:
	if drop_header:
	        knows_file.readline()
        for line in knows_file:
            line = line.strip().split(separator)
            current_tuple = [int(line[0]), int(line[1]), float(line[2])]
            trusts_rel[(current_tuple[0], current_tuple[1])] = (True, current_tuple[2])
    
    for person1 in people_rel:
        for person2 in people_rel:
            current_tuple = (person1, person2)
            if not current_tuple in trusts_rel:
                trusts_rel[current_tuple] = (False, problem.add_var())
    return people_rel, knows_rel, trusts_rel


def write_trust_mpe(k_fname, t_fname, people_rel, knows_rel, trusts_rel, problem):
    with open(k_fname, 'w') as k_f:
        print('id1,id2,value',file=k_f)
        for person1 in people_rel:
            for person2 in people_rel:
                (isconst, val) = knows_rel[(person1, person2)]
                if not isconst:
                    val = problem.solutions[val]
                print('%d,%d,%.3f' %(person1, person2, val),file=k_f)

    with open(t_fname, 'w') as t_f:
        print('id1,id2,value',file=t_f)
        for person1 in people_rel:
            for person2 in people_rel:
                (isconst, val) = trusts_rel[(person1, person2)]
                if not isconst:
                    val = problem.solutions[val]
                print('%d,%d,%.3f' %(person1, person2, val),file=t_f)


if __name__ == '__main__':
	exit(1)
