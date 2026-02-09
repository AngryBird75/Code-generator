class StackVM:
    def __init__(self):
        self.stack = []
        self.vars = {}

    def run(self, code):
        for instr in code:
            parts = instr.split()
            op = parts[0]
            if op == 'PUSH': self.stack.append(int(parts[1]))
            elif op == 'LOAD': self.stack.append(self.vars[parts[1]])
            elif op == 'STORE': self.vars[parts[1]] = self.stack.pop()
            elif op == 'ADD': b=self.stack.pop();a=self.stack.pop();self.stack.append(a+b)
            elif op == 'SUB': b=self.stack.pop();a=self.stack.pop();self.stack.append(a-b)
            elif op == 'MUL': b=self.stack.pop();a=self.stack.pop();self.stack.append(a*b)
            elif op == 'DIV': b=self.stack.pop();a=self.stack.pop();self.stack.append(a//b)
            elif op == 'PRINT': print(self.stack.pop())
