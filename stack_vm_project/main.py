from lexer import Lexer
from parser import Parser
from codegen import CodeGen
from vm import StackVM

with open("input.txt") as f:
    code = f.read()

# 1️⃣ Lexical Analysis
lexer = Lexer(code)
tokens = lexer.tokenize()
print("=== Tokens ===")
print(tokens)

# 2️⃣ Parsing
parser = Parser(tokens)
ast = parser.parse()
print("\n=== Parse Tree / AST ===")
for node in ast:
    print(node)

# 3️⃣ Code Generation
cg = CodeGen()
stack_code = cg.generate_all(ast)
print("\n=== Stack-Based Instructions ===")
for instr in stack_code:
    print(instr)

# 4️⃣ Execute VM
print("\n=== VM Output ===")
vm = StackVM()
vm.run(stack_code)
