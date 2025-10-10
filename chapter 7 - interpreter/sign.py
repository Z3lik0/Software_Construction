def sign(value):
    if value < 0:
        return -1
    else:
        return 1


def t_another():
    assert sign(-4) == -1

def t_minus_sign():
    assert sign(-3) == -1

def t_plus_sign():
    assert sign(19) == 1

def t_plus_sign_2():
    assert sign(-1) == 1

def t_plus_sign_3():
    printf()
    assert sign(1) == 1


def run_tests(all_tests):
    results = {"pass":0,"fail":0,"error":0}
    for test in tests:
        try:
            test()
            results["pass"] +=1
        except AssertionError:
            results["fail"] += 1
        except Exception:
            results["error"] += 1
    print(results)

def find_tests(prefix): # example prefix = "t_"
    tests = []
    for (name, func) in globals().items():
        if name.startswith(prefix):
            tests.append(func)
    return tests



if __name__ == "__main__":
    tests = find_tests("t_")
    run_tests(tests)
