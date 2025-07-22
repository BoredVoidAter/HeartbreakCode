
from heartbreak_code.tokenizer import Tokenizer
from heartbreak_code.parser import Parser
from heartbreak_code.interpreter import Interpreter

def run_heartbreak_code(source_code):
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()
    print("Tokens:", tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

    interpreter = Interpreter()
    interpreter.interpret(ast)

if __name__ == "__main__":
    code = """
The story of us is my_variable 1989
Speak Now: 'Hello, HeartbreakCode!'
Speak Now: my_variable

Would've my_variable is 1989 Speak Now:
    Speak Now: 'It was a good year!'
Could've my_variable is greater than 2000 Speak Now:
    Speak Now: 'Future vibes!'
Should've Speak Now:
    Speak Now: 'Somewhere in between.'
End Verse

Define Verse 'MyChorus': Speak Now:
    Speak Now: 'This is my chorus!'
End Verse

Perform 'MyChorus'
"""
    run_heartbreak_code(code)