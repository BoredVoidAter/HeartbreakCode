class ASTNode:
    pass

class AlbumDefinition(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class RecordInstantiation(ASTNode):
    def __init__(self, album_name, args):
        self.album_name = album_name
        self.args = args

class MemberAccess(ASTNode):
    def __init__(self, obj, member):
        self.obj = obj
        self.member = member

class TryCatchFinally(ASTNode):
    def __init__(self, try_body, catch_body, finally_body):
        self.try_body = try_body
        self.catch_body = catch_body
        self.finally_body = finally_body

class LinerNotesLiteral(ASTNode):
    def __init__(self, pairs):
        self.pairs = pairs

class LinerNotesAccess(ASTNode):
    def __init__(self, liner_notes, key):
        self.liner_notes = liner_notes
        self.key = key

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

class TracklistLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class TracklistAccess(ASTNode):
    def __init__(self, tracklist, index):
        self.tracklist = tracklist
        self.index = index

class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForLoop(ASTNode):
    def __init__(self, item_name, tracklist, body):
        self.item_name = item_name
        self.tracklist = tracklist
        self.body = body

class FunctionDefinition(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value

class FeatureImport(ASTNode):
    def __init__(self, file_name):
        self.file_name = file_name

class WaitFor(ASTNode):
    def __init__(self, task, callback_body):
        self.task = task
        self.callback_body = callback_body

class DecodeMessage(ASTNode):
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern

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
            if self.current_token.type == "COMMENT":
                self.eat("COMMENT")
                continue
            statements.append(self.parse_statement())
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
        if token.type == "STRING_SINGLE" or token.type == "STRING_DOUBLE":
            self.eat(token.type)
            return String(token.value.strip("'").strip('"'))
        elif token.type == "NUMBER":
            self.eat("NUMBER")
            return Number(int(token.value))
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            if self.current_token and self.current_token.type == "L_BRACKET":
                return self.tracklist_access(Identifier(token.value))
            return Identifier(token.value)
        elif token.type == "L_BRACKET":
            return self.tracklist_literal()
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
        
        self.eat("END_VERSE")
        return IfStatement(condition, Program(body), else_if_blocks, else_block)

    def tracklist_literal(self):
        self.eat("L_BRACKET")
        elements = []
        while self.current_token and self.current_token.type != "R_BRACKET":
            elements.append(self.expression())
            if self.current_token and self.current_token.type == "COMMA":
                self.eat("COMMA")
        self.eat("R_BRACKET")
        return TracklistLiteral(elements)

    def tracklist_access(self, tracklist_node):
        self.eat("L_BRACKET")
        index = self.expression()
        self.eat("R_BRACKET")
        return TracklistAccess(tracklist_node, index)

    def while_loop_statement(self):
        self.eat("ON_REPEAT_AS_LONG_AS")
        condition = self.comparison_expression()
        self.eat("SPEAK_NOW")
        body = []
        while self.current_token and self.current_token.type != "END_REPEAT":
            body.append(self.parse_statement())
        self.eat("END_REPEAT")
        return WhileLoop(condition, Program(body))

    def for_loop_statement(self):
        self.eat("FOR_EVERY")
        item_name = self.current_token.value
        self.eat("IDENTIFIER")
        self.eat("IN")
        tracklist = self.expression()
        self.eat("SPEAK_NOW")
        body = []
        while self.current_token and self.current_token.type != "END_TOUR":
            body.append(self.parse_statement())
        self.eat("END_TOUR")
        return ForLoop(item_name, tracklist, Program(body))

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
        elif self.current_token.type == "ON_REPEAT_AS_LONG_AS":
            return self.while_loop_statement()
        elif self.current_token.type == "FOR_EVERY":
            return self.for_loop_statement()
        elif self.current_token.type == "THE_FINAL_WORD_IS":
            return self.return_statement()
        elif self.current_token.type == "DEFINE_ALBUM":
            return self.album_definition()
        elif self.current_token.type == "NEW_RECORD_OF":
            return self.record_instantiation()
        elif self.current_token.type == "THIS_IS_ME_TRYING":
            return self.try_catch_finally_statement()
        elif self.current_token.type == "LINER_NOTES_ARE":
            return self.liner_notes_literal()
        elif self.current_token.type == "FEATURE":
            return self.feature_import_statement()
        elif self.current_token.type == "WAIT_FOR":
            return self.wait_for_statement()
        
        else:
            raise Exception(f"Unexpected token in parse_statement: {self.current_token.type}")

    def feature_import_statement(self):
        self.eat("FEATURE")
        file_name_token = self.current_token
        self.eat("STRING_SINGLE") # Ensure it's a string token
        file_name = file_name_token.value.strip("'").strip('"')
        return FeatureImport(file_name)

    def wait_for_statement(self):
        self.eat("WAIT_FOR")
        task = self.expression() # The expression representing the async task
        self.eat("THEN_SPEAK_NOW")
        callback_body = []
        while self.current_token and self.current_token.type != "END_AFTERGLOW":
            callback_body.append(self.parse_statement())
        self.eat("END_AFTERGLOW")
        return WaitFor(task, Program(callback_body))

    def decode_message_expression(self):
        self.eat("DECODE_MESSAGE")
        self.eat("FEATURING")
        self.eat("IDENTIFIER") # text=
        self.eat("EQUALS")
        text = self.expression()
        self.eat("COMMA")
        self.eat("IDENTIFIER") # pattern=
        self.eat("EQUALS")
        pattern = self.expression()
        return DecodeMessage(text, pattern)

    def function_definition(self):
        self.eat("DEFINE_VERSE")
        self.eat("STRING_SINGLE")
        name = self.tokens[self.position - 1].value.strip("''")
        parameters = []
        if self.current_token and self.current_token.type == "FEATURING":
            self.eat("FEATURING")
            while self.current_token and self.current_token.type == "IDENTIFIER":
                parameters.append(self.current_token.value)
                self.eat("IDENTIFIER")
                if self.current_token and self.current_token.type == "COMMA":
                    self.eat("COMMA")
        self.eat("COLON") # Eat the colon after function name/parameters
        self.eat("SPEAK_NOW")
        body = []
        while self.current_token and self.current_token.type != "END_VERSE":
            body.append(self.parse_statement())
        self.eat("END_VERSE")
        return FunctionDefinition(name, parameters, Program(body))

    def function_call(self):
        self.eat("PERFORM")
        self.eat("STRING_SINGLE")
        name = self.tokens[self.position - 1].value.strip("''")
        arguments = {}
        if self.current_token and self.current_token.type == "FEATURING":
            self.eat("FEATURING")
            while self.current_token and self.current_token.type == "IDENTIFIER":
                param_name = self.current_token.value
                self.eat("IDENTIFIER")
                self.eat("EQUALS")
                param_value = self.expression()
                arguments[param_name] = param_value
                if self.current_token and self.current_token.type == "COMMA":
                    self.eat("COMMA")
        return FunctionCall(name, arguments)

    def return_statement(self):
        self.eat("THE_FINAL_WORD_IS")
        value = self.expression()
        return ReturnStatement(value)

    def album_definition(self):
        self.eat("DEFINE_ALBUM")
        name = self.current_token.value
        self.eat("IDENTIFIER")
        self.eat("SPEAK_NOW")
        body = []
        while self.current_token and self.current_token.type != "END_ALBUM":
            body.append(self.parse_statement())
        self.eat("END_ALBUM")
        return AlbumDefinition(name, Program(body))

    def record_instantiation(self):
        self.eat("NEW_RECORD_OF")
        album_name = self.current_token.value
        self.eat("IDENTIFIER")
        args = {}
        if self.current_token and self.current_token.type == "FEATURING":
            self.eat("FEATURING")
            while self.current_token and self.current_token.type == "IDENTIFIER":
                param_name = self.current_token.value
                self.eat("IDENTIFIER")
                self.eat("EQUALS")
                param_value = self.expression()
                args[param_name] = param_value
                if self.current_token and self.current_token.type == "COMMA":
                    self.eat("COMMA")
        return RecordInstantiation(album_name, args)

    def try_catch_finally_statement(self):
        self.eat("THIS_IS_ME_TRYING")
        self.eat("SPEAK_NOW")
        try_body = []
        while self.current_token and self.current_token.type not in ("LOOK_WHAT_YOU_MADE_ME_DO", "ITS_OVER_NOW", "END_TRYING"):
            try_body.append(self.parse_statement())
        
        catch_body = None
        if self.current_token and self.current_token.type == "LOOK_WHAT_YOU_MADE_ME_DO":
            self.eat("LOOK_WHAT_YOU_MADE_ME_DO")
            self.eat("SPEAK_NOW")
            catch_body = []
            while self.current_token and self.current_token.type not in ("ITS_OVER_NOW", "END_TRYING"):
                catch_body.append(self.parse_statement())
            catch_body = Program(catch_body)

        finally_body = None
        if self.current_token and self.current_token.type == "ITS_OVER_NOW":
            self.eat("ITS_OVER_NOW")
            self.eat("SPEAK_NOW")
            finally_body = []
            while self.current_token and self.current_token.type != "END_TRYING":
                finally_body.append(self.parse_statement())
            finally_body = Program(finally_body)

        self.eat("END_TRYING")
        return TryCatchFinally(Program(try_body), catch_body, finally_body)

    def liner_notes_literal(self):
        self.eat("LINER_NOTES_ARE")
        self.eat("L_CURLY_BRACE")
        pairs = {}
        while self.current_token and self.current_token.type != "R_CURLY_BRACE":
            key = self.current_token.value
            self.eat("IDENTIFIER")
            self.eat("COLON")
            value = self.expression()
            pairs[key] = value
            if self.current_token and self.current_token.type == "COMMA":
                self.eat("COMMA")
        self.eat("R_CURLY_BRACE")
        return LinerNotesLiteral(pairs)

    def member_access(self, obj_node):
        self.eat("DOT")
        member_name = self.current_token.value
        self.eat("IDENTIFIER")
        return MemberAccess(obj_node, member_name)

    def expression(self):
        token = self.current_token
        if token.type == "STRING_SINGLE" or token.type == "STRING_DOUBLE":
            self.eat(token.type)
            return String(token.value.strip("'").strip('"'))
        elif token.type == "NUMBER":
            self.eat("NUMBER")
            return Number(int(token.value))
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            if self.current_token and self.current_token.type == "L_BRACKET":
                return self.tracklist_access(Identifier(token.value))
            elif self.current_token and self.current_token.type == "DOT":
                return self.member_access(Identifier(token.value))
            return Identifier(token.value)
        elif token.type == "L_BRACKET":
            return self.tracklist_literal()
        elif token.type == "LINER_NOTES_ARE":
            return self.liner_notes_literal()
        elif token.type == "DECODE_MESSAGE":
            return self.decode_message_expression()
        else:
            raise Exception(f"Expected an expression, got {token.type}")