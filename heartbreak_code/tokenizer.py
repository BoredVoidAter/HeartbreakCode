
import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Tokenizer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.position = 0
        self.token_specs = [
            ("SKIP", r"\s+"),
            ("ASSIGN", r"The story of us is"),
            ("SPEAK_NOW", r"Speak Now:"),
            ("STRING", r"\'[^\']*\'|\"[^\"]*\""),
            ("NUMBER", r"\d+"),
            ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
            ("UNKNOWN", r"."),
        ]

    def tokenize(self):
        while self.position < len(self.source_code):
            match = None
            for token_type, pattern in self.token_specs:
                regex = re.compile(pattern)
                m = regex.match(self.source_code, self.position)
                if m:
                    match = m
                    if token_type != "SKIP":
                        self.tokens.append(Token(token_type, m.group(0)))
                    break
            if match:
                self.position = match.end(0)
            else:
                raise Exception(f"Unexpected character: {self.source_code[self.position]}")
        return self.tokens
