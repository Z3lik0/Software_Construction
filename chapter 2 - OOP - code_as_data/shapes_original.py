import math

class Shape():

    def __init__(self, name):
        self.name = name
    
    def perimeter(self):
        raise NotImplementedError("perimeter missing")
    
    def area(self):
        raise NotImplementedError("area missing")
    
    def density(self, weight):
        return weight / self.area()

class Square(Shape):
    
    def __init__(self, name, side):
        super().__init__(name)
        self.side = side

    def perimeter(self):
        return self.side * 4
    
    def area(self):
        return self.side ** 2
    
class Circle(Shape):

    def __init__(self, name, radius):
        super().__init__(name)
        self.radius = radius

    def perimeter(self):
        return 2 * math.pi * self.radius
    
    def area(self):
        return (self.radius ** 2) * math.pi
        


examples = [Square("square", 2), Circle("CR", 4)]



if __name__ == "__main__":
    for thing in examples:
        n = thing.name
        p = thing.perimeter()
        a = thing.area()
        print(f"{n} has perimeter {p:.2f} and area {a:.2f}")

