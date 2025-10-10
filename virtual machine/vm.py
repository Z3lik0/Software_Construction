import sys
from architecture import NUM_REG, OPS, OP_MASK, OP_SHIFT, OP_WIDTH, RAM_LEN

COLUMNS = 4
DIGITS = 8

class VirtualMachine:

    def __init__(self):
        self.initialize([])
        self.prompt = ">>"
    
    def initialize(self, program):
        assert len(program) <= RAM_LEN, "Program is too large"
        self.ram = [
            program[i] if (i < len(program)) else 0
            for i in range(RAM_LEN)
        ]
        self.ip = 0
        self.reg = [0] * NUM_REG
    
    #2a0202
    #OP_MASK=0xFF
    #OP_SHIFT = 8  # shift up by one byte
    #OP_WIDTH = 6  # op width in characters when printing
    # 0 & 0 = 0         0 & 1 =0        1&0 = 0        1& 1 =1
    # 0000 0000 0000 0000 1111 1111  0xff
    # 0010 1010 0000 0010 0000 0010  2A0202
    # 
    def fetch(self):
        instruction = self.ram[self.ip]   #2a0202 #FF
        self.ip += 1
        op = instruction & OP_MASK  # 02
        instruction >>= OP_SHIFT
        arg0 = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg1 = instruction & OP_MASK
        return [op, arg0, arg1]
    
    def run(self):
        running = True
        while running:
            op, arg0, arg1 = self.fetch()
            if op == OPS["hlt"]["code"]:
                running = False
            elif op == OPS["ldc"]["code"]:
                constant = arg1
                register_index = arg0
                self.reg[register_index] = constant
            elif op == OPS["str"]["code"]:
                source_reg_idx = arg0
                dest_mem_reg_idx = arg1
                self.ram[self.reg[dest_mem_reg_idx]] = self.reg[source_reg_idx]
            elif op == OPS["prr"]["code"]:
                print(self.prompt, self.reg[arg0])
            elif op == OPS["beq"]["code"]:
                if self.reg[arg0] == 0:
                    self.ip = arg1
            else:
                assert False, "Unknown operation"
    
    def show(self, writer):
        # Show registers
        for (i, r) in enumerate(self.reg):
            print(f"R{i:06x} = {r:06x}", file=writer)

        # How much memory to show
        top = max(i for (i, m) in enumerate(self.ram) if m != 0)

        # Show memory
        base = 0
        while base <= top:
            output = f"{base:06x}: "
            for i in range(COLUMNS):
                output += f"  {self.ram[base + i]:06x}"
            print(output, file=writer)
            base += COLUMNS


def main():
    assert len(sys.argv) == 2, f"Usage ..."
    reader = open(sys.argv[1],"r")
    writer = sys.stdout
    lines = [ln.strip() for ln in reader.readlines()]
    program = [int(ln,16) for ln in lines]
    vm = VirtualMachine()
    vm.initialize(program)
    vm.run()
    vm.show(writer)


if __name__ == "__main__":
    main()