class Shape():
    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError("area")
        
    def perimeter(self):
        raise NotImplementedError("perimeter")

class Triangle(Shape):
    def __init__(self, name, a, b, c, h):
        super().__init__(name)
        self.a = a 
        self.b = b
        self.c = c
        self.h = h

    def perimeter(self):
        return self.a + self.b + self.c
    
    def area(self):
        A = self.b * self.h/2 
        return  A
    
class Square(Shape):
    def __init__(self, name, side):
        super().__init__(name)
        self.side = side
    
    def area(self):
        A = self.side ** 2
        return A
    
    def perimeter(self):
        return 4 * self.side

s1 = Square("S1", 3)
t1 = Triangle("T1", 3, 3, 3, 6)

# shapies = [s1, t1]

# for shape in shapies:
#     print(shape.name)
#     print(shape.perimeter())


def square_new(name, side):
    return {
        "name": name,
        "side": side,       
        "_class": "Square",
        "_parent": "Shape",
        "perimeter": square_perimeter,
        "area": square_area
    }


def square_perimeter(thing:dict):
    return 4*thing["side"]

def square_area(thing:dict):
    side = thing["side"]
    return side**2


def call(thing, method_name):
    return thing[method_name](thing) #calls method
    
examples = [square_new("sq0", 3), square_new("sq1", 8),]
for ex in examples:
    n = ex["name"]
    p = call(ex, "perimeter")
    a = call(ex, "area")
    print(n, p, a)


