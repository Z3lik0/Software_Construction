class Fake:
    def __init__(self,func=None,value=None):
        self.calls = []
        self.func = func
        self.value = value

    def __call__(self, *args, **kwds):
        self.calls.append([args,kwds])
        if self.value:
            return self.value
        return self.func(*args, **kwds)


def adder(a,b):
    return a + b

def fake_add(a,b):
    return a + 1

adder = Fake(adder,value=100)

print(adder(2,3))
print(adder(70,4))
print(adder.calls)