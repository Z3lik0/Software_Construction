import sys
import json


def do_sequenz(env,args):
    assert len(args) > 0
    result = None
    for expr in args:
        result = do(env,expr)
    return result


def do_setzen(env, args):
    assert len(args) == 2
    assert isinstance(args[0],str)
    var_name = args[0]
    value = do(env, args[1])
    env[var_name] = value
    return value


def do_bekommen(env, args):
    assert len(args) == 1
    assert isinstance(args[0],str)
    assert args[0] in env, f"Variable name {args[0]} not found"
    value = env[args[0]]
    return value


def do_addieren(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right


def do_betrag(env, args):
    assert len(args) == 1
    val = do(env,args[0])
    return abs(val)

def do_func(env, args):
    assert len(args) == 2
    parameters = args[0]
    body = args[1]
    return ["func", parameters, body]

### implement stacks ###

# 1. evaluate the arguments before even calling the function
# 2. look up the function based on its name
# 3. create a new environment
# 4. run the function
# 5. discard the environment
# 6. return the function results

def do_call(envs, args):
    ### set up call
    assert len(args) <= 1
    assert isinstance(args[0], str)
    name = args[0]
    values = [do(envs,a) for a in args[1:]] #get all values 

    ### find the function
    func = envs_get(name)
    assert isinstance(func,list) and func[0] == "func" #make sure it's still a function
    params, body = func[1], func[2]
    assert len(values) == len(params)

    ### create env for function

    # local_env = {} #solution without zip
    # for i, param  in enumerate(params):
    #     local_env[param] = values[i] 

    local_env = dict(zip(params, values))
    envs.append(local_env)
    result = do(envs,body)
    envs.pop() #bye to this stack frame / environment
    return result


# quicker but less readable way with zip
    # local_env = dict(zip(params, values))
    # result = do(env, body)
    # env.pop()

### using introspection to find all functions in the global scope <- more flexible
OPS = {name[3:]: func #so name is without "do_"
       for (name, func) in globals().items() 
       if name.startswith("do_")

}

### more understandable but less flexible

# OPS = { #operations
#     "addieren": do_addieren,
#     "betrag": do_betrag,
#     "setzen": do_setzen,
#     "bekommen": do_bekommen,
#     "sequenz": do_sequenz
#        }

def envs_get(envs, name): #envs = list of dictionaries [{#function_scope},{#global_scope}] 
    assert isinstance(name,str)
    for each_env in reversed(envs):
        if name in each_env:
            return each_env(name)



def do(env, expr):
    if isinstance(expr,int): #return integers
        return expr
    assert isinstance(expr,list)
    assert expr[0] in OPS, "Unknown operation"
    func = OPS[expr[0]]
    func(env, expr[1:])
    return func(env,expr[1:])

# def do(env, expr): # get rid of the if statements
#     if isinstance(expr,int):
#         return expr
#     assert isinstance(expr,list)
#     if expr[0] == "addieren":
#         return do_addieren(env, expr[1:])
#     if expr[0] == "betrag":
#         return do_betrag(env, expr[1:])
#     if expr[0] == "setzen":
#         return do_setzen(env, expr[1:])
#     if expr[0] == "bekommen":
#         return do_bekommen(env, expr[1:])
#     if expr[0] == "sequenz":
#         return do_sequenz(env,expr[1:])
#     assert False, "Unknown operation"


def main():
    program = ""
    assert len(sys.argv) == 2, "usage: python interpreter.py code.tll"
    with open(sys.argv[1], "r") as source:
        program = json.load(source)
    #print(program)
    result = do({}, program)
    print(result)


if __name__ == "__main__":
    main()