import numpy as np

def sort_dict(dict):
    sorted_dict = {}
    for w in sorted(dict,key=dict.get,reverse=True):
        sorted_dict.update({w:dict[w]})
    return sorted_dict

def zero_one(init_ans, restriction, restrict):
    excluded = []
    for i in range(len(init_ans)):
        if init_ans[i] == 1:
            pass
        if 0 < init_ans[i] < 1:
            excluded.append(i)
            init_ans[i] = 0.0
        else:
            init_ans[i] = 1.0
        if np.dot(init_ans, restriction) > restrict:
            init_ans[i] = 0.0
    return init_ans, excluded

def calc_opt(optimize, ans):
    return np.dot(optimize,ans)

def get_relaxed(weights_sorted, dropkeys, restrict, restriction, optimize):
    init_ans = np.zeros(len(optimize))
    restrict_left = restrict
    #使わないindexをのぞいておく
    index = [i for i in weights_sorted.keys() if i not in dropkeys]
    # print("index of vars to include => ", index)
    for i in index:
        if restrict_left <= 0:
            break
        #ウェイトの大きいものから1にできるか（できるならする）
        if restriction[i] <= restrict_left: 
            init_ans[i] = 1.0
            restrict_left -= restriction[i]
        else:
        #1にできなかったら少数に
            init_ans[i] = restrict_left/restriction[i]
            break
    return init_ans

def get_mask(excluded,restriction):
    mask = np.zeros(len(restriction))
    for i in excluded:
        mask[i] = 1.0
    return mask