from lexer import Lexer
from parser import Parser, Assign, BinOp, Num, Var, Print
from codegen import CodeGen
from vm import StackVM
from tabulate import tabulate


# 1️⃣ Read source code
with open("input.txt") as f:
    code = f.read()

# 2️⃣ Lexical Analysis
lexer = Lexer(code)
tokens = lexer.tokenize()

# --- Display Tokens in Table ---
table = [[i+1, t.type, t.value] for i, t in enumerate(tokens)]
print("\n=== Tokens (Lexemes) ===")
print(tabulate(table, headers=["#", "Type", "Value"], tablefmt="grid"))

# 3️⃣ Parsing
parser = Parser(tokens)
ast = parser.parse()

# --- AST Tree Printer ---
def print_ast(node, indent=""):
    if isinstance(node, list):
        for n in node:
            print_ast(n, indent)
    elif isinstance(node, Assign):
        print(f"{indent}Assign({node.var})")
        if node.expr: print_ast(node.expr, indent + "  ")
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp({node.op})")
        print_ast(node.left, indent + "  ")
        print_ast(node.right, indent + "  ")
    elif isinstance(node, Num):
        print(f"{indent}Num({node.value})")
    elif isinstance(node, Var):
        print(f"{indent}Var({node.name})")
    elif isinstance(node, Print):
        print(f"{indent}Print")
        if isinstance(node.expr, list):
            for e in node.expr:
                print_ast(e, indent + "  ")
        else:
            print_ast(node.expr, indent + "  ")

print("\n=== AST Tree ===")
print_ast(ast)

# 4️⃣ Code Generation
cg = CodeGen()
stack_code = cg.generate_all(ast)
print("\n=== Stack Instructions ===")
for instr in stack_code:
    print(instr)

# 5️⃣ Execute in VM
print("\n=== VM Output ===")
vm = StackVM()
vm.run(stack_code)
