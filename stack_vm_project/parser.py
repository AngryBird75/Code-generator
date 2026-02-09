from lexer import Token

# AST Node Classes
class Node: pass

class Num(Node):
    def __init__(self, value): self.value = value
    def __repr__(self): return f"Num({self.value})"

class Var(Node):
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Var({self.name})"

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self): return f"BinOp({self.left}, {self.op}, {self.right})"

class Assign(Node):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr
    def __repr__(self): return f"Assign({self.var}, {self.expr})"

class Print(Node):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self): return f"Print({self.expr})"

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token('EOF','')

    def eat(self, type_):
        if self.current().type == type_:
            self.pos += 1
        else:
            raise Exception(f"Expected {type_}, got {self.current().type}")

    # Expression parser
    def factor(self):
        tok = self.current()
        if tok.type == 'NUMBER':
            self.eat('NUMBER')
            return Num(tok.value)
        elif tok.type == 'ID':
            self.eat('ID')
            return Var(tok.value)

    def term(self):
        node = self.factor()
        while self.current().type in ('MUL','DIV'):
            op = self.current().type
            self.eat(op)
            node = BinOp(node, op, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current().type in ('PLUS','MINUS'):
            op = self.current().type
            self.eat(op)
            node = BinOp(node, op, self.term())
        return node

    # Parse a single statement
    def statement(self):
        tok = self.current()

        # Variable declaration
        if tok.type == 'TYPE':
            self.eat('TYPE')
            var_name = self.current().value
            self.eat('ID')
            self.eat('ASSIGN')
            node = self.expr()
            if self.current().type == 'SEMICOLON':
                self.eat('SEMICOLON')
            return Assign(var_name, node)

        # Assignment
        elif tok.type == 'ID':
            var_name = tok.value
            self.eat('ID')
            self.eat('ASSIGN')
            node = self.expr()
            if self.current().type == 'SEMICOLON':
                self.eat('SEMICOLON')
            return Assign(var_name, node)

        # Print
        elif tok.type == 'PRINT':
            self.eat('PRINT')
            var_tok = self.current()
            self.eat('ID')
            if self.current().type == 'SEMICOLON':
                self.eat('SEMICOLON')
            return Print(Var(var_tok.value))

    # Parse all statements
    def parse(self):
        ast = []
        while self.pos < len(self.tokens):
            ast.append(self.statement())
        return ast
