import numpy as np
from hfuncs import *
from math import floor

class BranchAndBound:
    def __init__(self, restriction, optimize, restrict):
        self.restrict = restrict
        self.restriction = np.array(restriction)
        self.optimize = np.array(optimize)
        self.weights = {i:optimize[i]/(restriction[i]+1e-6) for i in range(len(optimize))}
        self.weights_sorted = sort_dict(self.weights)

        self.init_opt = 0.0
        self.init_exclude = []
        self.init_ans = []
        
        self.pairs = {}
        
    def P(self, zeros, ones, initial=False):
        print("------doing P({}, {})-------"\
            .format(np.array(zeros)+1, np.array(ones)+1))
        restrict_left = self.restrict
        exclude = []
        exclude.extend(zeros)
        exclude.extend(ones)
        exclude = set(exclude)
        mask = get_mask(ones, self.restriction)
        
        restrict_left -= np.dot(self.restriction, mask)
        
        if restrict_left <= 0:
            print("restricl_left reached 0\n")
            return False, False
        
        ans = get_relaxed(self.weights_sorted, exclude, \
            restrict_left, self.restriction, self.optimize) + mask
        print("ans is     ", ans)
        
        opt = calc_opt(self.optimize, ans)
        print("opt is     ", opt)
        
        _, exclude_next = zero_one(ans, self.restriction, self.restrict)
        print("z_o_ans is ", _)
        
        if initial:
            self.init_ans, self.init_exclude = _, exclude_next
            self.init_opt = calc_opt(self.optimize, self.init_ans)
            print("init_opt is ", self.init_opt)
            print("init_ans is ", self.init_ans,"\n")
        else:
            if floor(opt) > self.init_opt:
                self.init_opt = floor(opt)
                self.pairs.update({floor(opt):ans})#best ans 更新
                print("new init_opt is", self.init_opt,"\n")
                return exclude_next, floor(opt)
            else:
                print("\n")
                return False, False
            
    def do_P(self, zeros, ones, exclude_next):
        if exclude_next:
            zeros_next = zeros + exclude_next
            exclude_next_z, new_opt_z = self.P(zeros_next, ones, False)
            
            ones_next = ones + exclude_next
            exclude_next_o, new_opt_o = self.P(zeros, ones_next, False)
            
            if exclude_next_z:
                self.do_P(zeros_next, ones, exclude_next_z)
            else:
                pass
            
            if exclude_next_o:
                self.do_P(zeros, ones_next, exclude_next_o)
            else:
                pass
        else:
            return False
        
    def initialize(self):
        print("initialize")
        self.P([], [], initial=True)
        
    # solve だけだとprintが出力されない
    def solve(self):
        self.do_P([], [], self.init_exclude)
            
            
        
# restriction = [2, 3, 1, 3]
# restrict = 4.0
# optimize = [3, 4, 1, 2]
restriction = [4, 5, 1, 3]
restrict = 6.0
optimize = [7, 8, 1, 2]

bb = BranchAndBound(restriction, optimize, restrict)
bb.initialize()
# bb.do_P([],[], [0])#分岐が両方終端してしまってもinit_optを更新してしまう
bb.do_P([], [], bb.init_exclude)

print("\nanswer pairs", bb.pairs)
# print("best opt", bb.init_opt)
        
        
        
        
        