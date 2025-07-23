
import json
import requests
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
        self.current_request = None # For The Setlist
        self.current_response = None # For The Setlist

    def execute_verse_by_name(self, verse_name):
        """Executes a HeartbreakCode verse by its name."""
        if verse_name not in self.functions:
            raise Exception(f"Undefined verse: {verse_name}")
        function_node = self.functions[verse_name]
        self.push_scope()
        # No arguments are passed when called from Setlist for now
        self.return_value = None
        self.visit(function_node.body)
        self.pop_scope()

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
        # Check if it's a built-in Greatest Hits function
        if hasattr(self.greatest_hits, node.name):
            method = getattr(self.greatest_hits, node.name)
            # Prepare arguments for the Greatest Hits method
            args = []
            kwargs = {}
            # Assuming Greatest Hits functions take positional arguments or keyword arguments
            # This part needs to be carefully aligned with how GreatestHits methods are defined
            # For simplicity, we'll pass all arguments as keyword arguments if they are named
            # Otherwise, we'll try to pass them positionally if the method expects it.
            # A more robust solution would involve inspecting the method signature.
            for param_name, param_value_node in node.arguments.items():
                kwargs[param_name] = self.visit(param_value_node)
            
            try:
                return method(**kwargs)
            except TypeError as e:
                # If keyword arguments don't match, try positional if no kwargs were intended
                if not kwargs and node.arguments:
                    # This is a heuristic and might need refinement based on actual GreatestHits methods
                    positional_args = [self.visit(arg_node) for arg_node in node.arguments.values()]
                    return method(*positional_args)
                else:
                    raise Exception(f"Error calling Greatest Hits function '{node.name}': {e}")

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

    def visit_ReadTheLetter(self, node):
        file_path = self.visit(node.file_path)
        if not isinstance(file_path, str):
            raise Exception("Type error: 'Read The Letter' expects a string for file path.")
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {e}")

    def visit_WriteInTheDiary(self, node):
        file_path = self.visit(node.file_path)
        content = self.visit(node.content)
        if not isinstance(file_path, str):
            raise Exception("Type error: 'Write In The Diary' expects a string for file path.")
        if not isinstance(content, str):
            raise Exception("Type error: 'Write In The Diary' expects a string for content.")
        try:
            with open(file_path, 'w') as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"Error writing to file {file_path}: {e}")

    def visit_DoesTheVaultContain(self, node):
        file_path = self.visit(node.file_path)
        if not isinstance(file_path, str):
            raise Exception("Type error: 'Does The Vault Contain' expects a string for file path.")
        return os.path.exists(file_path)

    def visit_SpillYourGuts(self, node):
        user_input = input()
        self.assign_variable(node.variable_name, user_input)

    def visit_TellMeWhy(self, node):
        print("\n--- Debugger (Tell Me Why) ---")
        print("Current variables:")
        for scope in self.scopes:
            for var_name, var_value in scope.items():
                print(f"  {var_name}: {var_value}")
        print("-----------------------------")
        while True:
            command = input("Debugger (type 'continue' to resume): ").strip()
            if command == "continue":
                break
            elif command.startswith("inspect "):
                var_name = command.split(" ", 1)[1]
                try:
                    value = self.resolve_variable(var_name)
                    print(f"  {var_name}: {value}")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("Unknown command. Type 'continue' to resume or 'inspect <variable_name>' to inspect a variable.")
        print("--- Resuming execution ---")

    def visit_SendMessage(self, node):
        url = self.visit(node.url)
        method = self.visit(node.method).upper()
        headers = self.visit(node.headers) if node.headers else {}
        body = self.visit(node.body) if node.body else None

        if not isinstance(url, str):
            raise Exception("Type error: URL must be a string.")
        if not isinstance(method, str):
            raise Exception("Type error: Method must be a string.")
        if not isinstance(headers, dict):
            raise Exception("Type error: Headers must be Liner Notes.")

        try:
            response = None
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=body)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=body)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, json=body)
            else:
                raise Exception(f"Unsupported HTTP method: {method}")

            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            # Return response as Liner Notes
            return {
                "__type__": "LinerNotes",
                "status_code": response.status_code,
                "headers": response.headers,
                "text": response.text,
                "json": response.json() if response.headers.get('Content-Type') == 'application/json' else None
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Web request failed: {e}")

    def visit_UntangleStory(self, node):
        json_string = self.visit(node.json_string)
        if not isinstance(json_string, str):
            raise Exception("Type error: 'Untangle The Story' expects a string.")
        try:
            data = json.loads(json_string)
            # Convert JSON object/array to Liner Notes/Tracklist
            if isinstance(data, dict):
                liner_notes = {"__type__": "LinerNotes"}
                for key, value in data.items():
                    liner_notes[key] = value
                return liner_notes
            elif isinstance(data, list):
                return data # HeartbreakCode Tracklist is a Python list
            else:
                return data # Primitive types
        except json.JSONDecodeError as e:
            raise Exception(f"JSON decoding failed: {e}")

    def visit_WeaveStory(self, node):
        data = self.visit(node.liner_notes_or_tracklist)
        if isinstance(data, dict) and data.get("__type__") == "LinerNotes":
            # Remove internal type key before serialization
            data_to_serialize = {k: v for k, v in data.items() if k != "__type__"}
            return json.dumps(data_to_serialize)
        elif isinstance(data, list):
            return json.dumps(data)
        else:
            raise Exception("Type error: 'Weave The Story' expects Liner Notes or a Tracklist.")

    def visit_LookInTheMirror(self, node):
        target = self.visit(node.target)
        aspect = node.aspect

        if isinstance(target, dict) and target.get("__type__") == "Record":
            album_name = target.get("__album_name__")
            if album_name not in self.albums:
                raise Exception(f"Album '{album_name}' not found for reflection.")
            album_node = self.albums[album_name]

            if aspect == "properties of":
                properties = []
                # Iterate through the album's body to find assignments (properties)
                for statement in album_node.body.statements:
                    if isinstance(statement, Assignment):
                        properties.append(statement.identifier)
                return properties
            elif aspect == "verses of":
                verses = []
                # Iterate through the album's body to find function definitions (verses)
                for statement in album_node.body.statements:
                    if isinstance(statement, FunctionDefinition):
                        verses.append(statement.name)
                return verses
            else:
                # Default: return all keys in the record instance (properties and potentially methods if stored directly)
                return list(target.keys())
        elif isinstance(target, dict) and target.get("__type__") == "LinerNotes":
            if aspect == "properties of":
                # For Liner Notes, properties are just the keys
                return [k for k in target.keys() if k != "__type__"]
            else:
                raise Exception("Liner Notes only support 'properties of' reflection.")
        else:
            raise Exception(f"Reflection not supported for type: {type(target).__name__}")

    # The Record Label: A Lyrical Package Manager
    def visit_InstallAlbum(self, node):
        album_name = self.visit(node.album_name)
        if not isinstance(album_name, str):
            raise Exception("Type error: 'Install Album' expects a string for album name.")
        self.greatest_hits.install_album(album_name)

    def visit_PublishAlbum(self, node):
        album_path = self.visit(node.album_path)
        if not isinstance(album_path, str):
            raise Exception("Type error: 'Publish Album' expects a string for album path.")
        self.greatest_hits.publish_album(album_path)

    def visit_SearchAlbums(self, node):
        query = self.visit(node.query)
        if not isinstance(query, str):
            raise Exception("Type error: 'Search Albums' expects a string for query.")
        self.greatest_hits.search_albums(query)

    # The Setlist: A Web Server Micro-framework
    def visit_DefineSetlistRoute(self, node):
        method = self.visit(node.method)
        path = node.path # Path is already a string from parser
        handler_verse_name = node.handler_verse_name # Handler verse name is already a string from parser
        if not isinstance(method, str):
            raise Exception("Type error: 'Define Setlist Route' expects a string for method.")
        self.greatest_hits.define_setlist_route(method, path, handler_verse_name)

    def visit_StartTheSetlist(self, node):
        port = self.visit(node.port) if node.port else 8000
        if not isinstance(port, int):
            raise Exception("Type error: 'Start The Setlist' expects a number for port.")
        self.greatest_hits.start_the_setlist(port)

    def visit_StopTheSetlist(self, node):
        self.greatest_hits.stop_the_setlist()

    def visit_SetlistResponseSend(self, node):
        content = self.visit(node.content)
        self.greatest_hits.setlist_response_send(content)

    def visit_SetlistResponseJson(self, node):
        data = self.visit(node.data)
        self.greatest_hits.setlist_response_json(data)

    def visit_SetlistResponseStatus(self, node):
        code = self.visit(node.code)
        if not isinstance(code, int):
            raise Exception("Type error: 'Setlist Response Status' expects a number for status code.")
        self.greatest_hits.setlist_response_status(code)

    def visit_SetlistRequestPath(self, node):
        return self.greatest_hits.setlist_request_path()

    def visit_SetlistRequestMethod(self, node):
        return self.greatest_hits.setlist_request_method()

    def visit_SetlistRequestBody(self, node):
        return self.greatest_hits.setlist_request_body()

    def visit_SetlistRequestHeader(self, node):
        header_name = self.visit(node.header_name)
        if not isinstance(header_name, str):
            raise Exception("Type error: 'Setlist Request Header' expects a string for header name.")
        return self.greatest_hits.setlist_request_header(header_name)

    # The Archives: Native Database Connectivity
    def visit_OpenTheArchives(self, node):
        db_name = self.visit(node.db_name)
        if not isinstance(db_name, str):
            raise Exception("Type error: 'Open The Archives' expects a string for database name.")
        self.greatest_hits.open_the_archives(db_name)

    def visit_CloseTheArchives(self, node):
        self.greatest_hits.close_the_archives()

    def visit_QueryTheArchives(self, node):
        query = self.visit(node.query)
        params = [self.visit(p) for p in node.params.elements] if node.params else ()
        if not isinstance(query, str):
            raise Exception("Type error: 'Query The Archives' expects a string for query.")
        return self.greatest_hits.query_the_archives(query, params)

    def visit_CreateArchiveTable(self, node):
        table_name = self.visit(node.table_name)
        columns = {k: self.visit(v) for k, v in node.columns.pairs.items()}
        if not isinstance(table_name, str):
            raise Exception("Type error: 'Create Archive Table' expects a string for table name.")
        return self.greatest_hits.create_archive_table(table_name, columns)

    def visit_InsertIntoArchive(self, node):
        table_name = self.visit(node.table_name)
        data = {k: self.visit(v) for k, v in node.data.pairs.items()}
        if not isinstance(table_name, str):
            raise Exception("Type error: 'Insert Into Archive' expects a string for table name.")
        return self.greatest_hits.insert_into_archive(table_name, data)

    def visit_SelectFromArchive(self, node):
        table_name = self.visit(node.table_name)
        columns = self.visit(node.columns) if node.columns else '*'
        where_clause = self.visit(node.where_clause) if node.where_clause else None
        params = [self.visit(p) for p in node.params.elements] if node.params else ()
        if not isinstance(table_name, str):
            raise Exception("Type error: 'Select From Archive' expects a string for table name.")
        return self.greatest_hits.select_from_archive(table_name, columns, where_clause, params)

    def visit_UpdateArchive(self, node):
        table_name = self.visit(node.table_name)
        set_clause = self.visit(node.set_clause)
        where_clause = self.visit(node.where_clause)
        params = [self.visit(p) for p in node.params.elements] if node.params else ()
        if not isinstance(table_name, str):
            raise Exception("Type error: 'Update Archive' expects a string for table name.")
        return self.greatest_hits.update_archive(table_name, set_clause, where_clause, params)

    def visit_DeleteFromArchive(self, node):
        table_name = self.visit(node.table_name)
        where_clause = self.visit(node.where_clause)
        params = [self.visit(p) for p in node.params.elements] if node.params else ()
        if not isinstance(table_name, str):
            raise Exception("Type error: 'Delete From Archive' expects a string for table name.")
        return self.greatest_hits.delete_from_archive(table_name, where_clause, params)
