import sys
import json

#python3 interpreter.py code.tll 


### specific functions ###
#what addieren(add) does
def do_addieren(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right

#what betrag (abs) does
def do_betrag(env, args):
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)

#what setzen (set) does
def do_setzen(env, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    var_name = args[0]
    value = do(env, args[1])
    env[var_name] = value
    return value

#what bekommen (get) does 
def do_bekommen(env, args):
    assert len(args) == 1
    assert args[0] in env, "Variable name {args[0]} not found."
    assert isinstance(args[0],str)
    value =env[args[0]]
    return value

#what sequence does <- run code sequentially (line by line)
def do_sequenz(env, args):
    assert len(args) > 0
    result = None
    for expr in args:
        result = do(env, expr)
        return result

##### #################### ####

### general functions  ###

#universal function used in main()
def do(env, expr): #gets expression
    #return integer 
    if isinstance(expr, int):
        return expr
    #is it list?
    assert isinstance(expr, list)
    if expr[0] == "addieren":
        return do_addieren(env, expr[1:])
    
    if expr[0] == "betrag":
        return do_betrag(env,expr[1:])
    
    if expr[0] == "setzen":
        return do_setzen(env,expr[1:])
    
    if expr[0] == "sequenz":
        return do_sequenz(env, expr[1:])


def main(): ##called every time we use interpreter
    program = ""
    assert len(sys.argv) == 2, "usage: python interpreter.py code.tll"  #we need at least [python interpreter.py, code.tll] [language, interpreter, file we want to interpret]
    with open(sys.argv[1], "r") as source:
        program = json.load(source)
        #print(program)
        result = do({}, program)
        
        print(result)
##### #################### ####

if __name__ == "__main__": ##called every time we use interpreter
    main()
