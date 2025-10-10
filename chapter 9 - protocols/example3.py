class Example:

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("you are exiting the protocol")

    def __init__(self):
        print("you create the object")

    def __enter__(self):
        print("you are entering the protocol")
    
    

# e = Example()
# e.__enter__()
# print("......")
# print("hello world")
# e.__exit__()

with Example() as e:     # e = Example() ; e.__enter__()
    print("......")
    print("hello world") # afterwards -> e.__exit__()


# with open("folder/example1.py","r") as f:   # f = open("e1.py","r") ; f.__enter__()
#     r = f.readlines()
#     print(r)                     # f.__exit__()

print("we are done")