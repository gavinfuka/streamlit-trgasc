from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial
import numpy as np
class RSEstimator:
    def __init__(self,x,y):
        self.x = np.array(x)
        self.y = np.array(y)
        poly = lagrange(x, y)
        self.Coef = Polynomial(poly).coef
        self.CoefLen = len(Polynomial(poly).coef)

    def EstSmith(self,price):
        result = 0
        for i,coef in enumerate(self.Coef):
            power = self.CoefLen-i-1
            result +=coef * (price ** power)
        if result >= 99 :
            return 99 
        return result