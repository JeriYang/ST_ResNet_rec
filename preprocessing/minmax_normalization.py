"""
    数据特征缩放
    MinMaxNormalization 使值变为-1到1 规则化，能更快得收敛
"""
import numpy as np
np.random.seed(1337)  # for reproducibility


class MinMaxNormalization(object):  # 转换到-1到1
    '''MinMax Normalization --> [-1, 1]
       x = (x - min) / (max - min).
       x = x * 2 - 1
    '''

    def __init__(self):
        pass

    def fit(self, X):  #找到最大，最小值
        self._min = X.min()
        self._max = X.max()
        print("min:", self._min, "max:", self._max)

    def transform(self, X): # 转换到-1到1之间，减少收敛速度
        X = 1. * (X - self._min) / (self._max - self._min)
        X = X * 2. - 1.
        return X

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X): #逆变换，由-1到1转化到对应的值
        X = (X + 1.) / 2.
        X = 1. * X * (self._max - self._min) + self._min
        return X


class MinMaxNormalization_01(object): # 转换到0到1
    '''MinMax Normalization --> [0, 1]
       x = (x - min) / (max - min).
    '''

    def __init__(self):
        pass

    def fit(self, X):
        self._min = X.min()
        self._max = X.max()
        print("min:", self._min, "max:", self._max)

    def transform(self, X):
        X = 1. * (X - self._min) / (self._max - self._min)
        return X

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X):
        X = 1. * X * (self._max - self._min) + self._min
        return X
