import sys
from architecture import NUM_REG, OPS, OP_MASK, OP_SHIFT, OP_WIDTH

class Assembler:
    
    def assemble(self,lines):
        instructions = self._get_lines(lines)
        compiled = [self._compile(instruction)
            for instruction in instructions]
        program = self._to_text(compiled)
        return program
    
    def _is_comment(self, line):
        return line.startswith("#")
    
    def _to_text(self,program):
        return [f"{op:06x}" for op in program]
    
    def _get_lines(self,lines):
        lines = [ln.strip() for ln in lines]
        lines = [ln for ln in lines if len(ln) > 0]
        lines = [ln for ln in lines if not self._is_comment(ln)]
        return lines
    
    def _combine(self, *args):
        result = 0
        for a in args:
            result <<= OP_SHIFT
            result |= a
        return result
    
    def _reg(self, token):
        assert token[0] == "R", f"Error"
        r = int(token[1:])
        assert 0 <= r < NUM_REG, "Out of bound register"
        return r
    
    def _compile(self,instruction):
        tokens = instruction.split()
        op = tokens[0]  # hlt
        args = tokens[1:]
        fmt = OPS[op]["fmt"]
        op_code = OPS[op]["code"]

        if fmt == "--":
            return self._combine(op_code)
        elif fmt == "r-":
            return self._combine(self._reg(args[0]), op_code)
        else:
            assert False, "Finish the implementation!!"





def main(assembler_cls):
    assert len(sys.argv) == 2, f"Usage: {sys.argv[0]} input|-"
    reader = open(sys.argv[1], "r") if (sys.argv[1] != "-") else sys.stdin
    writer = sys.stdout
    lines = reader.readlines()
    assembler = assembler_cls()  # assembler = Assembler()
    program = assembler.assemble(lines)
    for instruction in program:
        print(instruction, file=writer)

if __name__ == "__main__":
    main(Assembler)