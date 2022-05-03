import datetime


class P:
    def __init__(self, x):
        self.lac = x
    @property
    def x(self):
        return self.__x
    @x.setter
    def lac(self, x):
        if x < 0:
            self.__x = 0
        elif x > 1000:
            self.__x = 1000
        else:
            self.__x = x


p1 = P(1001)
print(p1.x)

