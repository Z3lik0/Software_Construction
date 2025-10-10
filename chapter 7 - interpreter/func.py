def add(p1,p2):
    r = p1 + p2
    return r

def abs_(p1):
    if p1 > 0:
        return p1
    else:
        return -p1


## testing sum of 2 positive numbers
# 2 and 3
expected_result = 5
actual_result = add(2,3)
assert actual_result == expected_result, "we have a problem"


expected_result = 1
actual_result = abs_(-1)
assert actual_result == expected_result

