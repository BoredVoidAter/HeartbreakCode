
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

# Tracklist Example
The story of us is eras_tour_setlist ['Lover', 'Fearless', 'evermore']
Speak Now: eras_tour_setlist
Speak Now: eras_tour_setlist[0]
Speak Now: eras_tour_setlist[2]

# While Loop Example
The story of us is counter 0
On Repeat as long as counter is less than 3: Speak Now:
    Speak Now: counter
    The story of us is counter counter + 1
End Repeat

# For Loop Example
For every song in eras_tour_setlist: Speak Now:
    Speak Now: song
End Tour

# Function with Parameters and Return Value Example
Define Verse 'WriteASong' Featuring title, artist: Speak Now:
    Speak Now: 'Writing a song called '
    Speak Now: title
    Speak Now: ' by '
    Speak Now: artist
    The final word is title
End Verse

The story of us is my_song_title Perform 'WriteASong' Featuring title='All Too Well', artist='Taylor Swift'
Speak Now: 'The song I wrote is: '
Speak Now: my_song_title
"""
    run_heartbreak_code(code)