import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"{self.type}:{self.value}"

class Lexer:
    TOKEN_SPEC = [
        ('TYPE', r'int'),          # Must come before ID
        ('PRINT', r'print'),       # Must come before ID
        ('NUMBER', r'\d+'),
        ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('ASSIGN', r'='),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MUL', r'\*'),
        ('DIV', r'/'),
        ('SEMICOLON', r';'),
        ('SKIP', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]

    def __init__(self, code):
        self.code = code

    def tokenize(self):
        token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.TOKEN_SPEC)
        tokens = []
        for mo in re.finditer(token_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                tokens.append(Token(kind, int(value)))
            elif kind in ('ID','ASSIGN','PLUS','MINUS','MUL','DIV','TYPE','PRINT','SEMICOLON'):
                tokens.append(Token(kind, value))
            elif kind == 'SKIP':
                continue
            else:
                raise RuntimeError(f"Unexpected token: {value}")
        return tokens
