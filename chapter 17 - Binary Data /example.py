import struct

#0b11101101 <- 8 bits 
#metadata: 0b1110 <- 0 is separator between metadata & data
#data 1101
#every continuation byte starts with 10
# string_input = "hello world"
# fmt = f"iif{len(string_input)}s" #i = int, f= float, n = number of s = string characters
# a = 31
# b = 65
# c = 56
# d = bytes(string_input, "utf-8")

# binary = struct.pack(fmt,a, b, c, d)
# print("binary representation", repr(binary))

# unpacked = struct.unpack(fmt, binary)
# print(unpacked)
# with open("gruezi.txt", "r") as f:
#     content = f.read() 
#     print((content))

def pack_string(as_string):
    as_bytes = bytes(as_string, "utf-8")
    header = struct.pack("i", len(as_bytes)) #store header as integers in binary -> #i struct.pack("i", 6)
    format = f"{len(as_bytes)}s" #unpacking format based on length of string #5s 
    body = struct.pack(format, as_bytes)
    return header + body #header tells how to unpack it, body is what we want to unpack #pack("5s", "hello!")

def unpack_string(buffer):
    header, body = buffer[:4], buffer[4:] #first 4 bytes = header
    length = struct.unpack("i", header)[0]
    format = f"{length}s"
    result = struct.unpack(format, body)[0] #bcs struct gives an array back
    return str(result, "utf-8")


if __name__ == "__main__":
    result = pack_string("1grüezi!")
    print(repr(result))

    print(unpack_string(result))



