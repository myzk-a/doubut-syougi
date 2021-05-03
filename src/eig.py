import numpy as np

A = np.array([[5, 2],[2,8]])
l, v = np.linalg.eig(A)

print(l)
print(v)