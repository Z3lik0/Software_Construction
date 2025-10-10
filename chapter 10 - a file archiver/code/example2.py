class Adder:
    def __init__(self, value):
        self.value = value
        self.all_calls = []
    
    def __call__(self,another_value):
        self.all_calls.append(another_value)
        return self.value + another_value


add_3 = Adder(3)
result = add_3(45)
for i in range(4):
    result = add_3(i)
    print(f"Result is {result}")

print(f"I have been called with values: {add_3.all_calls}")