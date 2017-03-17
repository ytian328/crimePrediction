from sklearn.gaussian_process.kernels import Matern

import numpy as np

matern = Matern()
x = np.array([[1,2,3]])
y = np.array([[2,3,4]])

print(matern.__call__(x,y))

