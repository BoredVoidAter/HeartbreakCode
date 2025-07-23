
import os
import re
import time # For simulating async operations

from heartbreak_code.greatest_hits import GreatestHits
from heartbreak_code.tokenizer import Tokenizer
from heartbreak_code.parser import Parser

class Interpreter:
    def __init__(self):
        self.scopes = [{}]
        self.functions = {}
        self.albums = {}
        self.return_value = None
        self.greatest_hits = GreatestHits(self)

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

    def visit_AlbumDefinition(self, node):
        self.albums[node.name] = node

    def visit_RecordInstantiation(self, node):
        if node.album_name not in self.albums:
            raise Exception(f"Undefined Album: {node.album_name}")

        album_node = self.albums[node.album_name]
        record_instance = {"__type__": "Record", "__album_name__": node.album_name}
        
        self.push_scope() # New scope for record properties
        self.current_scope["this"] = record_instance # 'this' refers to the current record instance

        # Process album body to define properties and methods
        self.visit(album_node.body)

        # Assign arguments to record properties
        for param_name, param_value_node in node.args.items():
            record_instance[param_name] = self.visit(param_value_node)

        self.pop_scope()
        return record_instance

    def visit_MemberAccess(self, node):
        obj = self.visit(node.obj)
        member = node.member

        if isinstance(obj, dict) and obj.get("__type__") == "Record":
            if member in obj:
                return obj[member]
            elif member in self.functions: # Check for methods defined globally
                # For now, methods are just global functions. In a more complex system,
                # methods would be defined within the AlbumDefinition.
                return self.functions[member]
            else:
                raise Exception(f"Undefined member '{member}' for Record of Album '{obj.get('__album_name__')}'")
        elif isinstance(obj, dict) and obj.get("__type__") == "LinerNotes":
            if member in obj:
                return obj[member]
            else:
                raise Exception(f"Undefined key '{member}' in Liner Notes.")
        else:
            raise Exception(f"Cannot access members of type {type(obj).__name__}")

    def visit_TryCatchFinally(self, node):
        try:
            self.visit(node.try_body)
        except Exception as e:
            if node.catch_body:
                self.push_scope()
                self.current_scope["error"] = str(e) # Make error message available in catch block
                self.visit(node.catch_body)
                self.pop_scope()
            else:
                raise e # Re-raise if no catch block
        finally:
            if node.finally_body:
                self.visit(node.finally_body)

    def visit_LinerNotesLiteral(self, node):
        liner_notes = {"__type__": "LinerNotes"}
        for key, value_node in node.pairs.items():
            liner_notes[key] = self.visit(value_node)
        return liner_notes

    def visit_LinerNotesAccess(self, node):
        liner_notes = self.visit(node.liner_notes)
        key = self.visit(node.key)
        if not isinstance(liner_notes, dict) or liner_notes.get("__type__") != "LinerNotes":
            raise Exception(f"Type error: {liner_notes} is not Liner Notes.")
        if key not in liner_notes:
            raise Exception(f"Key '{key}' not found in Liner Notes.")
        return liner_notes[key]

    def visit_FeatureImport(self, node):
        file_path = node.file_name
        # Assuming HeartbreakCode files have a .hc extension and are in the same directory
        full_path = os.path.join(os.path.dirname(__file__), f"{file_path}.hc")
        if not os.path.exists(full_path):
            raise Exception(f"Module not found: {full_path}")

        with open(full_path, "r") as f:
            module_code = f.read()

        # Tokenize and parse the imported module
        tokenizer = Tokenizer(module_code)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        module_ast = parser.parse()

        # Create a new interpreter instance for the module to avoid scope pollution
        module_interpreter = Interpreter()
        module_interpreter.interpret(module_ast)

        # Expose module's global variables, functions, and albums
        # This is a simplified approach; a real module system might be more selective
        for var_name, var_value in module_interpreter.scopes[0].items():
            self.assign_variable(var_name, var_value)
        for func_name, func_node in module_interpreter.functions.items():
            self.functions[func_name] = func_node
        for album_name, album_node in module_interpreter.albums.items():
            self.albums[album_name] = album_node

    def visit_WaitFor(self, node):
        # Simulate an asynchronous task
        task_result = self.visit(node.task)
        print(f"Performing asynchronous task: {task_result}")
        time.sleep(1) # Simulate delay
        print("Asynchronous task completed.")

        # Execute the callback body
        self.push_scope()
        self.visit(node.callback_body)
        self.pop_scope()

    def visit_DecodeMessage(self, node):
        text = self.visit(node.text)
        pattern = self.visit(node.pattern)

        if not isinstance(text, str) or not isinstance(pattern, str):
            raise Exception("Type error: 'Decode The Message' expects strings for text and pattern.")

        match = re.search(pattern, text)
        if match:
            return match.group(0) # Return the first match
        return None # No match found
