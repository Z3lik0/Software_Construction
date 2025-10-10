def sign(value):
    if value < 0:
        return -1
    else:
        return 1
    
assert sign(-3) == -1
assert sign(19) == 1

# put previous assertions within functions that we define as test functions

def t_minus_sign():
        assert sign(-3) == -1 #pass

def t_plus_sign():
        assert sign(19) == 1 #pass

def t_plus_sign_2():
        assert sign(1) == 1 #pass

# def t_plus_sign_3():
#         printf()
#         assert sign(1) == 1 #error

def t_plus_sign_sad():
        assert sign(-1) == 1 #fail


### run tests function for feedback! ###
def run_tests(all_tests):
    results = {"pass":0, "fail": 0, "error":0}

    for test in all_tests:
        try:
            test()
            results["pass"] +=1
        except AssertionError:
            results["fail"] += 1

        except Exception:
            results["error"] += 1
    print(results)


### using prefixes to separate tests from non-tests
def find_tests(prefix): #example prefix = t_
    tests = []
    for (name, func) in globals().items():
        if name.startswith(prefix):
              tests.append(func)
    return tests
              


if __name__ == "__main__":
    #tests= [ t_minus_sign, t_plus_sign_sad, t_plus_sign, t_plus_sign_2] #assertion by itself stops the execution (which we don't want here)
    #run_tests(find_tests("t_")) #find test automatically so you dont have to update list
    tests = find_tests("t_")
    run_tests(tests)