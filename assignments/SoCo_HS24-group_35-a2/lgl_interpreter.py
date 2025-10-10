import sys
import json
import random
import datetime
import time

logstring="id,timestamp,function_name,event\n"



class Environment:
    def __init__(self, name=None, parent=None):
        self.variables = {}
        self.parent = parent
        self.name = name

    def get(self, name):
        """Recursively retrieves a variable from the environment or its parent."""
        if name in self.variables:
            return self.variables[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            raise NameError(f"Name '{name}' not found")

    def set(self, name, value):
        """Sets a variable in the current environment."""
        self.variables[name] = value
        


def do_infix(env_, args):
    if isinstance(args[1], str) and args[1] in "* / + -".split(" "):
        return do_infix_arith(env_, args)
        #return OPS["infix_arith"](env_, expr)

    if isinstance(args[1], str) and args[1] in ["AND", "OR", "XOR"]:
        return do_infix_bool(env_, args)
        #return OPS["infix_bool"](env_, expr)


def do_infix_arith(env_, args):
    """
    Handles 'infix' math operations; e.g., [1, "+", 2] or [2, "*", 3]

    Returns
    -------
    int
        outcome of arithmetic operation ( * / + - )
    """
    left = do(env_, args[0])
    operation = args[1]
    right = do(env_, args[2])
    return eval(f"{left}{operation}{right}")

def do_infix_bool(env_, args):
    """
    Handles 'infix' boolean operations; e.g., [1, "AND", 0]
    ∗ AND: 1 AND 1 = 1, otherwise 0.
    ∗ OR: 1 OR 0 = 1, 0 OR 1 = 1, 0 OR 0 = 0, and 1 OR 1 = 1.
    ∗ XOR: 1 XOR 1 = 0, 0 XOR 0 = 0, 1 XOR 0 = 1, and 0 XOR 1 = 1.

       Returns
    -------
    bool
        outcome of a boolean operation
    """
    left = do(env_, args[0])
    bool_op = args[1]
    right = do(env_, args[2])

    if bool_op == "AND": # left AND right == 1
        return left == right == 1
    if bool_op == "OR": #EITHER left or right == 1
        return left == 1 or right == 1
    if bool_op == "XOR": #only left OR right == 1
        return (left == 1 and right == 0) or (left == 0 and right == 1)

def do_power(env_, args):
    """
    Handles 'power' ; e.g., 2^3 = ["power", 2, 3]
    
    Returns
    -------
    int 
        result of power operation
    """
    base = do(env_, args[0])
    exponent = do(env_, args[1])
    return base**exponent

def do_add(env_, args):
    """Handles the 'add' operation; e.g., ["add",1,2]

    Parameters
    ----------
    env_ : list
        The stack with the environments
    args : list
        The list of the two values to add
        (they can be other operations)

    Returns
    -------
    int
        the sum of the two values
    """

    assert len(args) == 2
    left = do(env_, args[0])
    right = do(env_, args[1])
    return left + right


def do_absolute_value(env_, args):
    """Handles the 'absolute_value' operation; e.g., ["absolute_value",-1]

    Parameters
    ----------
    env_ : list
        The stack with the environments
    args : object
        The value for which to compute
        the absolute number

    Returns
    -------
    int
        the absolute number the value
    """

    assert len(args) == 1
    val = do(env_, args[0])
    return abs(val)


def do_seq(env_, args):
    """Handles the 'seq' operation

    Example:
    ["seq",
        ["set", "alpha", 1],
        ["get", "alpha"]
    ]

    Parameters
    ----------
    env_ : list
        The stack with the environments
    args : list
        The list of operations to execute

    Returns
    -------
    int
        the return value of the last operation
        in the list of args
    """
    assert len(args) > 0
    result = None
    #original_env_= env_
    for expr in args:
        result = do(env_, expr)
    #    env_=original_env_
    return result


def do_set(env_, args):
    """Handles the 'set' operation; e.g., ["set", "alpha", 1]

    Parameters
    ----------
    env_ : list
        The stack with the environments
        where to store/update the variable
    args : list
        args[0] : name of variable
        args[1] : content of variable

    Returns
    -------
    int
        the value associated to the var
    """

    assert len(args) == 2
    assert isinstance(args[0], str)
    var_name = args[0]
    
    
    value = do(env_, args[1])
    env_.set(var_name, value)
    #print(f"DEBUG: Setting {var_name} to {value} in environment {env_.name}")
    return value



def do_get(env_, args):
    """Handles the 'get' operation; e.g., ["get", "alpha"]

    Parameters
    ----------
    env_ : list
        The stack with the environments
        from which to retrieve the variable
    args : str
        The name of the variable

    Returns
    -------
    object
        the content of the variable
    """

    assert len(args) == 1
    assert isinstance(args[0], str)
    var_name = args[0]
    value = env_.get(var_name)
    #print(f"DEBUG: Getting {var_name}, found {value} in environment {env_.name}")
    return value




def do_func(env_, args):
    """Handles the 'func' operation; ["func", "n", ["get","n"]]

    This function does not do much: it only
    prepares the data structure to store in
    memory, which can then be called later

    Parameters
    ----------
    env_ : list
        The stack with the environments
        (only here for consistency)
    args : list
        args[0] : parameters of the function
        args[1] : body of the function

    Returns
    -------
    list
        the list with parameters and body
    """

    assert len(args) == 2
    parameters = args[0]
    body = args[1]
    # Shallow Copy of env_,
    # so that env and stack_envs are two different lists in memory
    # env = env_[:]
    #return ["func", parameters, body, env]
    
    

    return ["func", env_, parameters, body]





# Initialize the log file with headers
def log_event(func_id, function_name, event):
    global logstring
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    logstring+=f"{func_id},{timestamp},{function_name},{event}\n"
    


def wrap(func):

    def _inner(env_, args):
        # Generate a unique ID for this function call
        func_id = random.randint(100000, 999999)
        
        # Log the start event
        log_event(func_id, args[0], "start")
        
        # Call the actual function
        result = func(env_, args)
        
        # Log the stop event
        #time.sleep(3) -> to check if time works-> works
        log_event(func_id, args[0], "stop")
        
        return result
    return _inner


@wrap
def do_call(env_, args):
    """Handles the 'call' operation; e.g., ["call","add_two",3,2]

    where "add_two" is the name of a function
    previously defined, and the rest are the
    arguments to pass to the function

    Parameters
    ----------
    env_ : list
        The stack with the environments,
        to which it pushes the specific env
        for the function when called and
        pop it afterwards
    args : list
        args[0] : name of function to call
        args[1] : arguments to pass to func

    Returns
    -------
    object
        the return value of the body execution
    """
    # setting up the call
    assert len(args) >= 1
    assert isinstance(args[0], str)
    func_name = args[0]  # "add_two"
    arguments = [do(env_, a) for a in args[1:]]  # [3, 2]

    # find the function
    func = env_.get(func_name)
    #print(f"DEBUG: Calling {func_name}...")
    assert isinstance(func, list) and func[0] == "func", \
            f"{func_name} is not a function!"
    
    
    prev_env=func[1]
    params = func[2]  # ["num1","num2"]
    body = func[3]  # ["add","num1","num2"]
    
    
    local_env = Environment(name=f"_{func_name}", parent=prev_env)

    # if there is no argument, we have nothing to add to 'local_env'.
    if isinstance(arguments[0], list) and len(arguments[0]) == 0:
        result = do(local_env, body)
    else:
        assert len(arguments) == len(params), \
                f"{func_name} receives a different number of parameters: \
                    params:{params}; arguments: {arguments}"
        # create the env for the function
        # params = ["num1","num2"], values = [3, 2]
        # env = {"num1":3, "num2":2}
    for param, arg in zip(params, arguments):
        local_env.set(param, arg)
    
    #print(f"working with this environment: {local_env.name}, {local_env.variables}")
    
    result = do(local_env, body)
    return result


def do(env_, expr):
    """Executes the given expression

    Our minimal operation is an integer value; everything else is
    then computed to a value.

    Parameters
    ----------
    env_ : list
        The stack with the environments
    operation : object
        operation to be executed

    Returns
    -------
    object
        value of the computed operation
    """
    if isinstance(expr, int):
        return expr
    
    #(if you accidentally forget to write ["get", a] and write "a"):
    if isinstance(expr, str):
        return env_.get(expr)

    assert isinstance(expr, list), f"Expression must be a list, got {type(expr)}"

    # For function calls, if the list of arguments is empty, return an empty list
    if len(expr) == 0:
        return []

    if isinstance(expr[1], str) and expr[1] in "* / + - AND OR XOR".split(" "):
        assert len(expr) == 3, f"Wrong number of arguments {expr}"
        return do_infix(env_, expr)

        #return OPS["infix"](env_, expr)


    # print(f"    DEBUG: {expr}")
    # print(f"    DEBUG: envs: {env_}")
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    operation = OPS[expr[0]]
    
    return operation(env_, expr[1:])


# dynamically find and name all operations we support in our language
OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}


def main():
    """Executes the interpreter on the given code file.
    
    The function also creates the global environment and the stack of
    environments, which will be then passed around. It prints the result
    of the computation.
    
    """
    program = ""
    if len(sys.argv) not in [2, 3, 4]:
        print("Usage: python3 lgl_interpreter.py <example_filename>")
        print("   or: python3 lgl_interpreter.py <example_filename> --trace trace_file.log")
        print("   e.g.: python3 lgl_interpreter.py example_trace.gsc --trace trace_file.log")
        print("   e.g.: python3 lgl_interpreter.py example_trace_ours.gsc --trace trace_file.log")
        sys.exit(1)
    
    with open(sys.argv[1], "r") as source:
        program = json.load(source)
    
    ### Tracing
    # Check if want to trace from command line
    #trace_file = "trace_file.log"#setting this name as a default, if you don't want to specify a name
    if len(sys.argv) > 2 and sys.argv[2] == "--trace":
        if len(sys.argv) > 3:
            trace_file=sys.argv[3]
        else:
            trace_file = "trace_file.log"
    else:
        trace_file = None
    
    global_env = Environment(name="global") # first environment we use
    result = do(global_env, program)
    print(result)

    ### Tracing
    # If trace_file is specified, open it and print result into it
    global logstring
    if trace_file:
        with open(trace_file, "w") as trace:
            trace.write(logstring)

if __name__ == "__main__":
    main()
