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
            ("WOULD_HAVE", r"Would've"),
            ("COULD_HAVE", r"Could've"),
            ("SHOULD_HAVE", r"Should've"),
            ("IS_GREATER_THAN_OR_EQUAL_TO", r"is greater than or equal to"),
            ("IS_LESS_THAN_OR_EQUAL_TO", r"is less than or equal to"),
            ("IS_GREATER_THAN", r"is greater than"),
            ("IS_LESS_THAN", r"is less than"),
            ("IS_NOT", r"is not"),
            ("IS", r"is"),
            ("DEFINE_VERSE", r"Define Verse"),
            ("END_VERSE", r"End Verse"),
            ("PERFORM", r"Perform"),
            ("STRING_SINGLE", r"'[^']*'),
            ("STRING_DOUBLE", r'"[^"]*"'),
            ("NUMBER", r"\d+"),
            ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
            ("L_BRACKET", r"["),            ("R_BRACKET", r"]"),            ("COMMA", r","),            ("ON_REPEAT_AS_LONG_AS", r"On Repeat as long as"),            ("END_REPEAT", r"End Repeat"),            ("FOR_EVERY", r"For every"),            ("IN", r"in"),            ("END_TOUR", r"End Tour"),            ("FEATURING", r"Featuring"),            ("THE_FINAL_WORD_IS", r"The final word is"),            ("EQUALS", r"="),
            ("DOT", r"\."),
            ("COLON", r":"),
            ("L_CURLY_BRACE", r"{"),
            ("R_CURLY_BRACE", r"}"),
            ("DEFINE_ALBUM", r"Define Album"),
            ("END_ALBUM", r"End Album"),
            ("THE_TRACKLIST_IS", r"The tracklist is"),
            ("THE_VERSES_ARE", r"The verses are"),
            ("NEW_RECORD_OF", r"a new Record of"),
            ("THIS_IS_ME_TRYING", r"This is me trying:"),
            ("LOOK_WHAT_YOU_MADE_ME_DO", r"Look what you made me do:"),
            ("ITS_OVER_NOW", r"It's over now:"),
            ("END_TRYING", r"End trying"),
            ("LINER_NOTES_ARE", r"Liner Notes are"),
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