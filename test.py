class A:
    b = 1
    def __init__(self) -> None:
        self.g = 2
    def func(self):
        return 1
    
    
class B(A):
    def func(self):
        print(super())
        f = super().func()
        return f

b = B()
print(B())
print('!' + str(b.func()))