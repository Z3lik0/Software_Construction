import datetime
import importlib
import sys

sys.modules["_datetime"] = None
importlib.reload(datetime)

today_ = datetime.date.today

f = open("filename.text", "r")
l = f.readlines()
f.close()

#with = a protocol is being followered

with open("filename.txt", "r") as f:
    # f.__enter__()  <- automatically runs in the background
    l = f.readlines()
    # f.__exit__() <- automatically runs in the background


class Fake:
    def __init__(self,name_repl,func=None,value=None):
        self.calls = []
        self.func = func
        self.value = value
        self.name_repl = name_repl
        self.original = None

    def __call__(self, *args, **kwds):
        self.calls.append([args,kwds])
        if self.func:
            return self.func(*args, **kwds)
        if self.value:
            return self.value
        return None
    
    def __enter__(self):
        assert self.name_repl in globals()
        self.original = globals()[self.name_repl]
        globals()[self.name_repl] = self
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        globals()[self.name_repl] = self.original
        


class ChristmasDiscount:
    def apply_discount(self,amount):
        today = today_()
        discount_percentage = 0
        if today.month == 12 and today.day == 25:
            discount_percentage = 0.15
        return amount - (amount * discount_percentage)


def christmas_day():
    return datetime.date(2024,12,25)


def test_christmas_discount():
    d_obj = ChristmasDiscount()
    price = 100.0
    
    with Fake("today_",value=datetime.date(2024,12,25)) as fake:
        final_price = d_obj.apply_discount(price)
        #print(fake.calls)

    assert final_price == 85.0

def test_no_christmas():
    d_obj = ChristmasDiscount()
    price = 100.0
    final_price = d_obj.apply_discount(price)
    assert final_price == 100.0


