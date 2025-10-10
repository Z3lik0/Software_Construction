class Archiver:
    def __init__(self, file):
        self.file = file

    def save_int(self, x):
        print(f"Saving an integer: {x}")

    def save_str(self, x):
        print(f"Saving a string: {x}")

    def save_bool(self, x):
        print(f"Saving a bool: {x}")

    def save_float(self, x):
        print(f"Saving a float: {x}")

    def save_list(self, x):
        print(f"Saving a list with {len(x)} rows.")

    def save(self, something):
        name = type(something).__name__
        string_ver_of_func = f"save_{name}"
        if hasattr(self, string_ver_of_func):
            method = getattr(self, string_ver_of_func)
            method(something)

# archiver = Archiver("file.txt")
# archiver.save(123)           # Calls save_int
# archiver.save("hello")       # Calls save_str
# archiver.save(True)          # Calls save_bool
# archiver.save(3.14)          # Calls save_float
# archiver.save([1, 2, 3])     # Calls save_list



def hide ( thing ) :
    def add_zero () :
        return thing
    def add_one () :
        return thing + 1
    return add_zero , add_one


secret = hide (1 + 2)
print ( " the secret number is " , secret [1]() )