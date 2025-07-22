
class Interpreter:
    def __init__(self):
        self.scope = {}
        self.functions = {}

    def interpret(self, ast):
        for statement in ast.statements:
            self.visit(statement)

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_Program(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Assignment(self, node):
        value = self.visit(node.value)
        self.scope[node.identifier] = value

    def visit_SpeakNow(self, node):
        value = self.visit(node.value)
        print(value)

    def visit_Identifier(self, node):
        if node.name in self.scope:
            return self.scope[node.name]
        else:
            raise Exception(f"Undefined variable: {node.name}")

    def visit_Number(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Comparison(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        operator = node.operator

        if operator == "is":
            return left_val == right_val
        elif operator == "is not":
            return left_val != right_val
        elif operator == "is greater than":
            return left_val > right_val
        elif operator == "is less than":
            return left_val < right_val
        elif operator == "is greater than or equal to":
            return left_val >= right_val
        elif operator == "is less than or equal to":
            return left_val <= right_val
        else:
            raise Exception(f"Unknown comparison operator: {operator}")

    def visit_IfStatement(self, node):
        if self.visit(node.condition):
            self.visit(node.body)
        else:
            executed_else_if = False
            for else_if_block in node.else_if_blocks:
                if self.visit(else_if_block.condition):
                    self.visit(else_if_block.body)
                    executed_else_if = True
                    break
            if not executed_else_if and node.else_block:
                self.visit(node.else_block)

    def visit_ElseIfStatement(self, node):
        # This will be handled by visit_IfStatement
        pass

    def visit_ElseStatement(self, node):
        self.visit(node.body)

    def visit_FunctionDefinition(self, node):
        self.functions[node.name] = node

    def visit_FunctionCall(self, node):
        if node.name in self.functions:
            function_node = self.functions[node.name]
            self.visit(function_node.body)
        else:
            raise Exception(f"Undefined function: {node.name}")
