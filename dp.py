import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy

n = int(input('Enter number of variables : '))
c_ = list(map(int,input("\nEnter objective function array : ").strip().split()))[:n]
a_ = list(map(int,input("\nEnter constraint function array : ").strip().split()))[:n]
restrict = int(input("\nEnter constraint : "))# we have restrict as int
assert restrict >= 0
c = np.array(c_, dtype='float')
a = np.array(a_, dtype='float')

# test
# c = np.array([7, 8, 1, 2], dtype='float') # maximize (objective function)
# a = np.array([4, 5, 1, 3], dtype='float') # (constraint function)
# restrict = 6 # constraint
# /test

# ---------------------J(k, θ)---------------------
# k is which item to use
# theta is the restrict (we make this larger on each iteration)

# J(k, θ) =  { J(k-1, θ)                                         (0 <= theta < a_k)
#            { max{ J(k-1, θ), c_k + J(k-1, θ-a_k) }                 (a_k <= theta)  

# ----------------------------------------------------

def calc_using(using, array):
#     using is a list with element indexes(starting at 1)
    if using:
        x = np.zeros(len(array))
        for i in using:
            x[i-1] = 1.0
        return np.dot(array, x)
    else:
        return 0

# for adding all computed Js 
# Js = {'(k, θ)':[calc_using([using], c), [using]]}
Js = {}

def J_1(a, c, restrict):
    for theta in range(restrict + 1):
        if theta < a[0]:
            using = []
        else:
            using = [1]
        Js.update({'({}, {})'.format(1, theta):[calc_using(using, c), using]})

# init Js with k = 1
J_1(a,c, restrict)

# for ease
def get_J(k, theta):
    return Js['({}, {})'.format(k, int(theta))]

# func for updating Js depending on condition
def J(k, theta, a, c):
    c_k = c[k-1]
    a_k = a[k-1]
    if theta < a_k:
        Js.update({'({}, {})'.format(k, theta):Js['({}, {})'.format(k-1, theta)]})
    else:
        choose = [get_J(k-1, theta)[0], c_k + get_J(k-1, theta-a_k)[0]]
        chosen = np.argmax(choose)
        
        if chosen == 0:
            using = copy.copy(get_J(k-1, theta)[1])
        else:
            using = copy.copy(get_J(k-1, theta-a_k)[1])
            using.append(k)#どんどん増えていくので何度も回さない
        Js.update({'({}, {})'.format(k, theta):[choose[chosen], using]}) 

# updating Js with k, θ
for k in range(2, len(a)+1):
    for theta in range(restrict+1):
        J(k, theta, a, c)
        
def sort_dict(dict):
    sorted_dict = {}
    for w in sorted(dict,key=dict.get,reverse=True):
        sorted_dict.update({w:dict[w]})
    return sorted_dict

final = {item[0]:item[1][0] for item in Js.items()}
final_dict = sort_dict(final)

print("\n{'(k, θ)' : objective} sorted ==> ")
print(final_dict)

