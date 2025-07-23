
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
# Variable Assignment
The story of us is my_variable 1989
Speak Now: 'Hello, HeartbreakCode!'
Speak Now: my_variable

# Conditional Logic
Would've my_variable is 1989 Speak Now:
    Speak Now: 'It was a good year!'
Could've my_variable is greater than 2000 Speak Now:
    Speak Now: 'Future vibes!'
Should've Speak Now:
    Speak Now: 'Somewhere in between.'
End Verse

# Function Definition and Call
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

# Album and Record Example
Define Album 'PopStar':
    The story of us is name 'Default Name'
    The story of us is age 0
    Define Verse 'Introduce': Speak Now:
        Speak Now: 'Hi, my name is '
        Speak Now: name
        Speak Now: ' and I am '
        Speak Now: age
        Speak Now: ' years old.'
    End Verse
End Album

The story of us is taylor a new Record of PopStar Featuring name='Taylor Swift', age=34
Perform 'Introduce' on taylor

# Error Handling Example
This is me trying: Speak Now:
    Speak Now: 'Attempting a risky operation...'
    The story of us is x 10 / 0 # This will cause an error
    Speak Now: 'This line will not be reached.'
Look what you made me do: Speak Now:
    Speak Now: 'An error occurred: '
    Speak Now: error
It's over now: Speak Now:
    Speak Now: 'Cleanup complete.'
End trying

# Liner Notes Example
The story of us is album_details Liner Notes are { title: 'Midnights', release_year: 2022, genre: 'Pop' }
Speak Now: album_details.title
Speak Now: album_details.release_year

# Greatest Hits Example
The story of us is original_text 'Hello World'
The story of us is upper_text Perform 'Change The Key' Featuring text=original_text, case_type='upper'
Speak Now: upper_text

The story of us is result Perform 'Calculate The Score' Featuring num1=10, num2=5, operation='add'
Speak Now: result

The story of us is num_string '123'
The story of us is converted_num Perform 'Rewrite History' Featuring value=num_string, target_type='number'
Speak Now: converted_num

# Collaborations: A Lyrical Module System
Feature 'my_module'

# The 'Afterglow': Asynchronous Operations
wait for 'long_running_task' Then Speak Now:
    Speak Now: 'Async task finished!'
End Afterglow

# Decoding The Message: Advanced String Pattern Matching
The story of us is secret_message 'The secret code is 123-ABC.'
The story of us is extracted_code Decode The Message Featuring text=secret_message, pattern="TEST"
Speak Now: 'Extracted code:'
Speak Now: extracted_code


"""
    run_heartbreak_code(code)