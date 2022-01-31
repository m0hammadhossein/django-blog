from django.test import TestCase


class A:
    def test(self):
        print('A')
        return super().test()

class B:
    def test(self):
        print('B')

class C:
    def test(self):
        print('C')

class test(A,B,C):
    pass

a=test()
print(a.test())