import re


string = "1+2+3*4/5-6"
numbers_filter = "\+|\-|\*|\/"
operators_filter = "[0-9]"
spl = re.split(operators_filter, string)


print(spl)