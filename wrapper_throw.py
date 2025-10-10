def wrapper(func):
    def _inner_workings(*args):
        
        frame_len = len(args[0]) + 2
        frame = "-" * frame_len
        print(frame)
        func(*args)
        print(frame)
    return _inner_workings

@wrapper
def our_func(a_message):
		print(a_message)

our_func("this is our message")




def my_wrapper(some_function):
    def stupid_closure(*args):
        frame_len = len("here's your dumb message:") + len(args[0]) + 2
        frame = f"◤{'━' * frame_len}◥"
        print(frame)
        some_function(*args)
        print(frame)
    return stupid_closure
@my_wrapper
def function_being_wrapped(dumb_message_that_will_be_wrapped):
    print(f"here's your dumb message: {dumb_message_that_will_be_wrapped}")

function_being_wrapped("I don't like this at all and I still don't see its use")



#a new wrapper

def newest_wrapper(func):
    def actual_wrapper(x):        
        print("▒▒▒▒▒▒▒▒▒▒   0%")
        print(func(x))
        print("██████████ 100%")
    return actual_wrapper

def load_content(x):
    return(x)

loader = newest_wrapper(load_content)
loader("𝐍𝐨𝐰 𝐥𝐨𝐚𝐝𝐢𝐧𝐠. . .")



#last_wrapper

def yet_another_wrapper(func, top="◤━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◥", bottom="◤━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◥"):
    def wrapper(x):
        print(top)
        print(func(x))
        print(bottom)
    return wrapper

@yet_another_wrapper
def gimme_gimme_gimme(message):
    return(message)

gimme_gimme_gimme("god")

