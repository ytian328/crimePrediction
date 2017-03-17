from sklearn.gaussian_process.kernels import Matern
from sklearn.gaussian_process.kernels import RBF

class Matern:
    def __init__(self, nu):
        self.nu = nu
        self.matern = Matern(nu)

    def __call__(self, x, y):
        """

        :param x:
        :param y:
        :return: matern covariance k(x, y)
        """

        return self.matern.__call__(x, y)

class RBF:
    def __init__(self):