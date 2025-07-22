
class Interpreter:
    def __init__(self):
        self.scopes = [{}]
        self.functions = {}
        self.return_value = None

    @property
    def current_scope(self):
        return self.scopes[-1]

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def resolve_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Undefined variable: {name}")

    def assign_variable(self, name, value):
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        self.current_scope[name] = value

    def interpret(self, ast):
        self.visit(ast)

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
        self.assign_variable(node.identifier, value)

    def visit_SpeakNow(self, node):
        value = self.visit(node.value)
        print(value)

    def visit_Identifier(self, node):
        return self.resolve_variable(node.name)

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

    def visit_TracklistLiteral(self, node):
        return [self.visit(element) for element in node.elements]

    def visit_TracklistAccess(self, node):
        tracklist = self.visit(node.tracklist)
        index = self.visit(node.index)
        if not isinstance(tracklist, list):
            raise Exception(f"Type error: {tracklist} is not a tracklist.")
        if not isinstance(index, int):
            raise Exception(f"Type error: Tracklist index must be an integer, got {type(index).__name__}.")
        if index < 0 or index >= len(tracklist):
            raise Exception(f"Index out of bounds: Tracklist has {len(tracklist)} elements, but index {index} was requested.")
        return tracklist[index]

    def visit_WhileLoop(self, node):
        while self.visit(node.condition):
            self.visit(node.body)

    def visit_ForLoop(self, node):
        tracklist = self.visit(node.tracklist)
        if not isinstance(tracklist, list):
            raise Exception(f"Type error: Cannot iterate over non-tracklist type {type(tracklist).__name__}.")
        for item in tracklist:
            self.push_scope()
            self.current_scope[node.item_name] = item
            self.visit(node.body)
            self.pop_scope()

    def visit_FunctionDefinition(self, node):
        self.functions[node.name] = node

    def visit_FunctionCall(self, node):
        if node.name not in self.functions:
            raise Exception(f"Undefined function: {node.name}")

        function_node = self.functions[node.name]
        self.push_scope()
        
        # Assign arguments to parameters in the new scope
        if len(node.arguments) != len(function_node.parameters):
            raise Exception(f"Function '{node.name}' expects {len(function_node.parameters)} arguments, but {len(node.arguments)} were provided.")

        for param_name in function_node.parameters:
            if param_name not in node.arguments:
                raise Exception(f"Missing argument for parameter '{param_name}' in function call to '{node.name}'.")
            self.current_scope[param_name] = self.visit(node.arguments[param_name])

        self.return_value = None  # Reset return value before function execution
        self.visit(function_node.body)
        self.pop_scope()
        return self.return_value

    def visit_ReturnStatement(self, node):
        self.return_value = self.visit(node.value)
        # In a real interpreter, you might want to stop execution of the current function here
        # For simplicity, we'll just set the return_value and let the function continue if there's more code
        # A more robust solution would involve raising a special exception to unwind the stack.
