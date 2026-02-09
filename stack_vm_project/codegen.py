from parser import Num, Var, BinOp, Assign, Print

class CodeGen:
    def __init__(self):
        self.instructions = []

    def generate(self, node):
        if isinstance(node, Num):
            self.instructions.append(f"PUSH {node.value}")
        elif isinstance(node, Var):
            self.instructions.append(f"LOAD {node.name}")
        elif isinstance(node, BinOp):
            self.generate(node.left)
            self.generate(node.right)
            if node.op == 'PLUS': self.instructions.append("ADD")
            elif node.op == 'MINUS': self.instructions.append("SUB")
            elif node.op == 'MUL': self.instructions.append("MUL")
            elif node.op == 'DIV': self.instructions.append("DIV")
        elif isinstance(node, Assign):
            self.generate(node.expr)
            self.instructions.append(f"STORE {node.var}")
        elif isinstance(node, Print):
            self.generate(node.expr)
            self.instructions.append("PRINT")

    def generate_all(self, ast):
        for node in ast:
            self.generate(node)
        return self.instructions
