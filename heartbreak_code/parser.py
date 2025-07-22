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

class IfStatement(ASTNode):
    def __init__(self, condition, body, else_if_blocks=None, else_block=None):
        self.condition = condition
        self.body = body
        self.else_if_blocks = else_if_blocks if else_if_blocks is not None else []
        self.else_block = else_block

class ElseIfStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ElseStatement(ASTNode):
    def __init__(self, body):
        self.body = body

class Comparison(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class FunctionDefinition(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name):
        self.name = name

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
            elif self.current_token.type == "WOULD_HAVE":
                statements.append(self.conditional_statement())
            elif self.current_token.type == "DEFINE_VERSE":
                statements.append(self.function_definition())
            elif self.current_token.type == "PERFORM":
                statements.append(self.function_call())
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

    def comparison_expression(self):
        left = self.expression()
        operator_token = self.current_token
        if operator_token.type in ("IS", "IS_NOT", "IS_GREATER_THAN", "IS_LESS_THAN", "IS_GREATER_THAN_OR_EQUAL_TO", "IS_LESS_THAN_OR_EQUAL_TO"):
            self.eat(operator_token.type)
            right = self.expression()
            return Comparison(left, operator_token.value, right)
        else:
            raise Exception(f"Expected a comparison operator, got {operator_token.type}")

    def conditional_statement(self):
        self.eat("WOULD_HAVE")
        condition = self.comparison_expression()
        self.eat("SPEAK_NOW") # Assuming 'Speak Now:' introduces the block
        body = []
        while self.current_token and self.current_token.type not in ("COULD_HAVE", "SHOULD_HAVE", "END_VERSE"): # End Verse is a placeholder for now
            body.append(self.parse_statement())
        
        else_if_blocks = []
        while self.current_token and self.current_token.type == "COULD_HAVE":
            self.eat("COULD_HAVE")
            else_if_condition = self.comparison_expression()
            self.eat("SPEAK_NOW")
            else_if_body = []
            while self.current_token and self.current_token.type not in ("COULD_HAVE", "SHOULD_HAVE", "END_VERSE"):
                else_if_body.append(self.parse_statement())
            else_if_blocks.append(ElseIfStatement(else_if_condition, Program(else_if_body)))

        else_block = None
        if self.current_token and self.current_token.type == "SHOULD_HAVE":
            self.eat("SHOULD_HAVE")
            self.eat("SPEAK_NOW")
            else_body = []
            while self.current_token and self.current_token.type != "END_VERSE": # Assuming 'End Verse' marks the end of the conditional block
                else_body.append(self.parse_statement())
            else_block = ElseStatement(Program(else_body))
        
        return IfStatement(condition, Program(body), else_if_blocks, else_block)

    def parse_statement(self):
        if self.current_token.type == "ASSIGN":
            return self.assignment_statement()
        elif self.current_token.type == "SPEAK_NOW":
            return self.speak_now_statement()
        elif self.current_token.type == "WOULD_HAVE":
            return self.conditional_statement()
        elif self.current_token.type == "DEFINE_VERSE":
            return self.function_definition()
        elif self.current_token.type == "PERFORM":
            return self.function_call()
        else:
            raise Exception(f"Unexpected token in parse_statement: {self.current_token.type}")

    def function_definition(self):
        self.eat("DEFINE_VERSE")
        self.eat("STRING")
        name = self.tokens[self.position - 1].value.strip("'")
        self.eat("SPEAK_NOW") # Assuming 'Speak Now:' introduces the block
        body = []
        while self.current_token and self.current_token.type != "END_VERSE":
            body.append(self.parse_statement())
        self.eat("END_VERSE")
        return FunctionDefinition(name, Program(body))

    def function_call(self):
        self.eat("PERFORM")
        self.eat("STRING")
        name = self.tokens[self.position - 1].value.strip("'")
        return FunctionCall(name)