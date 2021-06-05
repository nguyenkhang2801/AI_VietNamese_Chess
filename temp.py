import copy
a = [
    [1,2,3,4],
    [1,2,3,4],
    [1,2,3,4],
    [1,2,3,4]
]
b = copy.deepcopy(a)
b[3][2] = 5
print(b)
print(a)