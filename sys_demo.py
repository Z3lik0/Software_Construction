import sys
import time

def wrap_with_time(func):
    def _inner(x):
        start_time = time.time()
        print(f"Counting from now!")
        print(f"------------------")
        print(func(x))
        print(f"------------------")
        print(f"Time elapsed:{time.time()-start_time:.5f}s" )
    return _inner

@wrap_with_time
def greet(name):
    return f"Hello {name}, hope you're having a good study session!"

# greeting_wrapper = wrap_with_time(greet)


#dynamic dispatch using getattr instead of dictionary:



def main():
    assert len(sys.argv)> 1, "Usage: python3 sys_demo.py Ana Richard Beta 'I love me some kitty catty kit cat with the kids cat and lets see if this takes longer in any"
    for arg in sys.argv:
        greet(arg)

main()
    
        
    