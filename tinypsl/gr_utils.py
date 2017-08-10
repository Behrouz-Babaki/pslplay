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

def read_link_data(knows_fname, knows_target_fname, likes_fname, lived_fname, problem):
    people_dict = dict()
    people_id_dict = dict()
    
    interest_dict = dict()
    interest_id_dict = dict()
    
    places_dict = dict()
    places_id_dict = dict()
    
    def dict_man(constant_dict, id_dict):
        def str2id(cstr):
            if cstr in constant_dict:
                return constant_dict[cstr]
            id = len(constant_dict)
            constant_dict[cstr] = id
            id_dict[id] = cstr
            return id
        return str2id
    
    people_id = dict_man(people_dict, people_id_dict)
    interest_id = dict_man(interest_dict, interest_id_dict)
    place_id = dict_man(places_dict, places_id_dict)
            
    knows_rel = dict()
    with open(knows_fname) as knows_file:
        for line in knows_file:
            line = line.strip()
            if not line: continue
            line = line.split()
            current_tuple = (people_id(line[0]), people_id(line[1]))
            knows_rel[current_tuple] = (True, 1.0)
            
            
    likes_rel = dict()
    with open(likes_fname) as likes_file:
        for line in likes_file:
            line = line.strip()
            if not line: continue
            line = line.split()            
            current_tuple = (people_id(line[0]), interest_id(' '.join(line[1:-1])))
            likes_rel[current_tuple] = (True, float(line[-1]))
            
    lived_rel = dict()
    with open(lived_fname) as lived_file:
        for line in lived_file:
            line = line.strip()
            if not line: continue
            line = line.split()            
            current_tuple = (people_id(line[0]), place_id(' '.join(line[1:])))
            lived_rel[current_tuple] = (True, 1.0)
            
            
    with open(knows_target_fname) as knows_file:
        for line in knows_file:
            line = line.strip()
            if not line: continue
            line = line.split()
            current_tuple = (people_id(line[0]), people_id(line[1]))
            knows_rel[current_tuple] = (False, problem.add_var())
            
    for person in people_id_dict:
        for interest in interest_id_dict:
            current_tuple = (person, interest)
            if not current_tuple in likes_rel:
                likes_rel[current_tuple] = (True, 0.0)
                
    for person in people_id_dict:
        for place in places_id_dict:
            current_tuple = (person, place)
            if not current_tuple in lived_rel:
                lived_rel[current_tuple] = (True, 0.0)
                
    return knows_rel, likes_rel, lived_rel, people_id_dict, interest_id_dict, places_id_dict

def write_link_mpe(knows_fname, people_id_dict, knows_rel, problem):
    with open(knows_fname, 'w') as k_f:
        for p1 in people_id_dict:
            for p2 in people_id_dict:
                if p1==p2: continue
                (isconst, val) = knows_rel[(p1, p2)]
                if not isconst:
                    val = problem.solutions[val]
                print("'%s','%s',%.16f"%(people_id_dict[p1], people_id_dict[p2], val),file=k_f)

if __name__ == '__main__':
    exit(1)
