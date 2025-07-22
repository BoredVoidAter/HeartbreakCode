
class Interpreter:
    def __init__(self):
        self.scope = {}

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
