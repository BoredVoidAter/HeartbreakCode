class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Assignment(ASTNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class SpeakNow(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if self.tokens else None

    def advance(self):
        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}")

    def parse(self):
        statements = []
        while self.current_token:
            if self.current_token.type == "ASSIGN":
                statements.append(self.assignment_statement())
            elif self.current_token.type == "SPEAK_NOW":
                statements.append(self.speak_now_statement())
            else:
                raise Exception(f"Unexpected token: {self.current_token.type}")
        return Program(statements)

    def assignment_statement(self):
        self.eat("ASSIGN")
        identifier_token = self.current_token
        self.eat("IDENTIFIER")
        value = self.expression()
        return Assignment(identifier_token.value, value)

    def speak_now_statement(self):
        self.eat("SPEAK_NOW")
        value = self.expression()
        return SpeakNow(value)

    def expression(self):
        token = self.current_token
        if token.type == "STRING":
            self.eat("STRING")
            return String(token.value.strip("'\""))
        elif token.type == "NUMBER":
            self.eat("NUMBER")
            return Number(int(token.value))
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return Identifier(token.value)
        else:
            raise Exception(f"Expected an expression, got {token.type}")