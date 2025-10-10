def save(thing, seen, writer): #thing = value, writer = where to save thing
    id_ = id(thing)
    if id_ in seen:
        print(f"alias:{id_}:", file=writer)
        return
    seen[id_] = thing
    #bool
    if isinstance(thing, bool):
        print(f"bool:{id_}:{thing}", file=writer) 
    #int
    elif isinstance(thing, int):
        print(f"int:{id_}:{thing}", file=writer)
    #str
    elif isinstance(thing, str):
        newl = "\n"
        print(f'str:{id_}:{len(thing.split(newl))}', file=writer)
        print(thing, file=writer)
    #list   
    elif isinstance(thing, list):
        print(f"list:{id_}:{len(thing)}", file=writer)
        for item in thing:
            save(item, seen, writer)

    elif isinstance(thing, dict):
        print(f"dict:{id_}:{len(thing)}", file = writer)
        for k, v in thing.items():
            save(k, seen, writer)
            save(v, seen, writer)
    else:
        raise ValueError("Unsupported data type")
    
seen = {}
# def type_bool(readerwriter, value, mode="r"):
#     if mode == "w":
#        print(f"bool:{value}", file=readerwriter)  
#     if mode == "r":
#         if value == "True":
#             return True
#         return False
def type_alias(seen, reader, value):
    assert id_ in seen, "Trying to load sth that doesn't exist."

def type_bool(seen, reader, value):
    if value == "True":
        return True
    return False

def type_str(seen, reader, value):
    t = []
    for _ in range(int(value)):
        t.append(reader.readline()[:-1])
    return " ".join(t)

def type_int(seen, reader, value):
    return int(value)

def type_list(seen, reader, value):
    return [load(seen, reader) for _ in range(int(value))]
    # l = []
    # for _ in range(int(value)):
    #     l.append(load(reader))
    # return l

def type_dict(seen, reader, value):
    d = {}
    for _ in range(int(value)):
        key_ = load(seen, reader)
        value_ = load(seen, reader)
        d[key_] = value_
    return d

_types = {
    name.replace("type_", ""): func
    for (name, func) in globals().items()
    if name.startswith("type_")
}

# _types = {
#     "bool" : _bool,
#     "int" : _int,
#     "str" : _str,
#     "list" : _list,
#     "dict" : _dict
    
# }

def load(seen, reader):
    line = reader.readline()[:-1] #skip all newline characters
    assert line, "Nothing to read"
    fields = line.split(":", maxsplit=2)
    assert len(fields) == 3, f"Badly formed line {line}"
    _type, id_, value = fields
    #use dictionary with functions to "translate" values
    assert _type in _types, f"Unknown Type {_type}"
    obj = _types[_type](reader, value)

    return seen(id(obj))

shared = ["content"]    
combined = [shared, shared]

a = True
b = "fourty\ntwobool:True"
l = [23, b] #in YAML key = list, value = len(list) --- example: list: 2 
l[0] = a
d = {
    "name" : "Alberto",
    "age" : 41,
    "list": l
}


with open("outputWithId.txt", "w") as file:
    save(combined, seen, file)


with open("outputWithId.txt", "r") as file:
    c = load(seen = {}, reader=file)

print(c)
