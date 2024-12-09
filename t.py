class A():
    def __init__(self):
        self.a = 1

a = A()

class b():
    def __init__(self, a: A):
        a.a = 2

b(a)

print(a.a)