import math

### Super Class ###


#thing is a dictionary we pass that contrains the methods
def shape_density(thing, weight):
    return weight / call(thing,"area")


Shape = {
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None
}

### Square Definition ###

def square_perimeter(thing):
    return 4*thing["side"]

def square_area(thing):
    return thing["side"] ** 2

def square_density(thing, weight):
    return weight / thing["area"](thing)

# class / methods dicitionary
Square = {
    "perimeter": square_perimeter,
    "area":  square_area,
    "_classname": "Square",
    "_parent": Shape
    }

# data dictionary 
def square_new(name, side):
    new_object = {
        "name": name, 
        "side": side,
        "_class": Square
    }
    return new_object

### ################### ###


### Circle Definition ###

def circle_perimeter(thing):
    return 2 * math.pi * thing["radius"]

def circle_area(thing):
    return thing["radius"] ** 2 * math.pi

Circle = {
    "perimeter": circle_perimeter,
    "area":  circle_area,
    "_classname": "Circle",
    "_parent": "Shape"

}

def circle_new(name, radius):
    new_object = {
        "name": name, 
        "radius": radius,
        "_class": Circle
    }
    return new_object

### ################# ###

### method call ###

def call(thing, key_name, *args):
    method = find(thing["_class"],key_name) #find methods function
    return method(thing, *args)

def find(cls:dict, key_name): #recursive function to find method within all parents classes
    if key_name in cls:
        return cls[key_name]
    if cls["_parent"]:
        return find(cls["_parent"], key_name) 
    raise NotImplemented("Missing method" + key_name)


### ################# ###


a_square = square_new("Quadrat", 30)
another_square = square_new("Quadrat2", 4)

# check whether they are the same
print(a_square["_class"] is another_square["_class"])
print("density: ", call(a_square, "density", 10))

#area = call(a_square, "area")
#print(area)


