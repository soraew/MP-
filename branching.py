import numpy as np
from hfuncs import *
from math import floor

optimize = np.array([3, 4, 1, 2])
restriction = np.array([2, 3, 1, 3])
restrict = 4.0
weights = {i:optimize[i]/(restriction[i]+1e-6) for i in range(len(optimize))}
weights_sorted = sort_dict(weights)

init_opt = 0.0

def P(zeros, ones, initial=False, optimize=optimize, weights_sorted=weights_sorted, restrict=restrict, init_opt=init_opt):
    print("doing P({}, {})".format(zeros, ones))
    restrict_left = restrict
    # print("init_opt",init_opt)
    
    exclude = []
    exclude.extend(zeros)
    exclude.extend(ones)
    exclude = set(exclude)
    
    mask = get_mask(ones, restriction)
    
    restrict_left -= np.dot(restriction, mask)
    if restrict_left <= 0:
        print("restrict has reached below 0")
        return False
    
    ans = get_relaxed(weights_sorted, exclude, restrict_left, restriction, optimize) + mask
    print("ans is", ans)
    
    opt = calc_opt(optimize, ans)
    
    _, exclude_next = zero_one(ans, restriction, restrict)
    
    if initial:
        init_ans, init_exclude = _, exclude_next
        init_opt = calc_opt(optimize, init_ans)
        return init_exclude, init_opt
    else:
        if floor(opt) > init_opt:
            print("going to next, opt is ", opt, "\n")
            print("exclude next ", exclude_next)
            return exclude_next
        else:
            print("ending, opt is ", opt, "\n")
            return False
        
    
init_exclude, init_opt = P([], [], True)
# exclude = P([1], [0], init_opt=init_opt)

def do_P(zeros, ones, exclude_next, init_opt=init_opt, optimize=optimize, \
    weights_sorted=weights_sorted, restrict=restrict):
    if exclude_next:
        print("exclude_next", exclude_next)
        zeros_next = zeros + exclude_next
        exclude_next_z = P(zeros_next, ones, init_opt=init_opt)
        
        ones_next = ones + exclude_next
        exclude_next_o = P(zeros, ones_next, init_opt=init_opt)
        
        if exclude_next_z:
            do_P(zeros_next, ones, exclude_next_z)
        else:
            pass
            
        if exclude_next_o:
            do_P(zeros, ones_next, exclude_next_o)
        else:
            pass
    else:
        return False
        
print(do_P([], [], init_exclude))

