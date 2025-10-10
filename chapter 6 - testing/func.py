def add(p1, p2):
    r = p1 + p2
    return r


def abs_(p1):
    if p1 > 0:
        return p1
    else:
        return -p1

def zero():
    print("zero")

def one():
    print("one")

def two():
    print("two")

def add(a,b):
    return a+b




### bad practices in testing ###
    
# c = add(2,3)
# print(c)

# ab = abs_(-1)
# print(ab)

# print(abs_(34))
# print(add(-1,-2))

### improved version ###

## testing sum of 2 positive numbers
# 2 and 3
expected_result = 5
actual_result = add(2,3)
assert actual_result == expected_result, "we have a problem"
# if not(actual_result == expected_result): # <- this means the same as assert
#     print("you have a problem")


## testing absolute value 
# absolute value of  -1 
expected_result = 1 
actual_result = abs_(-1)
assert actual_result == expected_result, "we have a problem"

