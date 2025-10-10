from lgl_interpreter import *

def test_infix_arith():
    program = [1, "+", 2]
    env = Environment(name="global")
    result = do(env, program)
    assert result == 3, f"Expected 3, got {result}"

def test_infix_bool():
    program = [1, "AND", 0]
    env = Environment(name="global")
    result = do(env, program)
    assert result == False, f"Expected False, got {result}"

def test_infix_with_seq():
    program = ["seq", [1, "+", 2]]
    env = Environment(name="global")
    result = do(env, program)
    assert result == 3, f"Expected 3, got {result}"

def test_infix_with_variables():
    program = ["seq", ["set", "a", 1], [["get", "a"], "+", 2]]
    env = Environment(name="global")
    result = do(env, program)
    assert result == 3, f"Expected 3, got {result}"

def test_nested_infix_function():
    program = ["seq", ["set", "fplus", ["func", ["num1", "num2"], ["num1", "+", "num2"]]], ["call", "fplus", 4, 1]]
    env = Environment(name="global")
    result = do(env, program)
    assert result == 5, f"Expected 5, got {result}"

def test_lexical_scoping():
    # Program 6: Should return 100 due to lexical scoping of the global x
    program = [
        "seq",
        ["set", "x", 100],
        ["set", "one", ["func", [], ["get", "x"]]],
        ["set", "two", ["func", [], ["seq", ["set", "x", 42], ["call", "one", []]]]],
        ["set", "main", ["func", [], ["call", "two", []]]],
        ["call", "main", []]
    ]
    env = Environment(name="global")
    result = do(env, program)
    assert result == 100, f"Expected 100, got {result}"

def test_lexical_scoping_2():
    # Program 7: Should return 42 due to local x passed as parameter in lexical scoping
    program = [
        "seq",
        ["set", "x", 100],
        ["set", "one", ["func", ["x"], ["get", "x"]]],
        ["set", "two", ["func", [], ["seq", ["set", "x", 42], ["call", "one", ["get", "x"]]]]],
        ["set", "main", ["func", [], ["call", "two", []]]],
        ["call", "main", []]
    ]
    env = Environment(name="global")
    result = do(env, program)
    assert result == 42, f"Expected 42, got {result}"
    
    
    
    
def test_lexical_scoping_nested_function():
    # This should return 10, as the inner function's assignment to `x` should not affect the outer `x`
    program = [
        "seq",
        ["set", "outer_func", ["func", [], 
            ["seq",
                ["set", "x", 10],  # Outer `x` is set to 10
                ["set", "inner_func", ["func", [], ["set", "x", 20]]],  # Inner `x` is set to 20, local to inner_func
                ["call", "inner_func", []],  # Call inner_func (which sets its own `x` to 20)
                ["get", "x"]  # Return the outer `x`, which should still be 10
            ]
        ]],
        ["call", "outer_func", []]  # Execute outer_func
    ]
    
    env = Environment(name="global")
    result = do(env, program)
    assert result == 10, f"Expected 10, got {result}"
    

# Run tests
if __name__ == "__main__":
    

    def find_tests(prefix="test_"):
        all_tests = {}
        for name, test in globals().items():
            if name.startswith(prefix) and name != "test_file": #module_name
                all_tests[name] = test
        return all_tests
    
    
    all_tests = find_tests()
    for test in all_tests.values():
        test()
    print("All tests passed!")
