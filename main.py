
from heartbreak_code.tokenizer import Tokenizer
from heartbreak_code.parser import Parser
from heartbreak_code.interpreter import Interpreter

def run_heartbreak_code(source_code):
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(ast)
    return interpreter # Return interpreter for Setlist to use

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
It's over now:
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

# The Vault: File System API
Write In The Diary 'my_secret_diary.txt' Featuring content='Dear Diary, today I learned about file I/O in HeartbreakCode.'
Speak Now: 'Wrote to my_secret_diary.txt'

The story of us is diary_content Read The Letter 'my_secret_diary.txt'
Speak Now: 'Content of diary:'
Speak Now: diary_content

The story of us is file_exists Does The Vault Contain 'my_secret_diary.txt'
Speak Now: 'Does my_secret_diary.txt exist?'
Speak Now: file_exists

The story of us is non_existent_file_exists Does The Vault Contain 'non_existent.txt'
Speak Now: 'Does non_existent.txt exist?'
Speak Now: non_existent_file_exists

# Spill Your Guts: Interactive Console Input
Speak Now: 'What's your favorite HeartbreakCode feature?'
Spill Your Guts favorite_feature
Speak Now: 'You said your favorite feature is:'
Speak Now: favorite_feature

# Tell Me Why: Interactive Debugging
The story of us is debug_variable 100
Tell Me Why
The story of us is debug_variable debug_variable + 50
Speak Now: 'Debug variable after increment:'
Speak Now: debug_variable



# The Record Label: A Lyrical Package Manager
Speak Now: '\n--- The Record Label ---'
Perform 'Install Album' Featuring album_name='PopAnthems'
Perform 'Publish Album' Featuring album_path='./my_new_album.hbc'
Perform 'Search Albums' Featuring query='love songs'

# The Archives: Native Database Connectivity
Speak Now: '\n--- The Archives ---'
Perform 'Open The Archives' Featuring db_name='my_heartbreak_db.db'
Perform 'Create Archive Table' Featuring table_name='songs', columns=Liner Notes are {id: 'INTEGER PRIMARY KEY', title: 'TEXT', artist: 'TEXT'}
Perform 'Insert Into Archive' Featuring table_name='songs', data=Liner Notes are {title: 'Love Story', artist: 'Taylor Swift'}
Perform 'Insert Into Archive' Featuring table_name='songs', data=Liner Notes are {title: 'Drivers License', artist: 'Olivia Rodrigo'}
The story of us is all_songs Perform 'Select From Archive' Featuring table_name='songs'
Speak Now: 'All Songs:'
Speak Now: all_songs
Perform 'Close The Archives'

# The Setlist: A Web Server Micro-framework
Speak Now: '\n--- The Setlist ---'

Define Verse 'HandleRoot': Speak Now:
    Speak Now: 'Handling root request!'
    The story of us is req_path Perform 'Setlist Request Path'
    Speak Now: 'Request Path:'
    Speak Now: req_path
    Perform 'Setlist Response Send' Featuring content='Hello from HeartbreakCode!'
End Verse

Define Verse 'HandleJson': Speak Now:
    Speak Now: 'Handling JSON request!'
    The story of us is req_method Perform 'Setlist Request Method'
    Speak Now: 'Request Method:'
    Speak Now: req_method
    The story of us is req_body Perform 'Setlist Request Body'
    Speak Now: 'Request Body:'
    Speak Now: req_body
    Perform 'Setlist Response JSON' Featuring data=Liner Notes are {message: 'This is a JSON response', status: 'success'}
End Verse

Perform 'Define Setlist Route' Featuring method='GET', path='/', for_verse='HandleRoot'
Perform 'Define Setlist Route' Featuring method='POST', path='/json', for_verse='HandleJson'
Perform 'Start The Setlist' Featuring port=8000
Speak Now: 'Web server started on http://localhost:8000. Press Ctrl+C to stop.'
# In a real scenario, you'd keep the interpreter running or have a mechanism to stop the server.
# For this example, we'll just let it start and then the script will exit.
# You can test by opening http://localhost:8000 in your browser or using curl.
# curl -X POST -H "Content-Type: application/json" -d "{\"key\":\"value\"}" http://localhost:8000/json
# Perform 'Stop The Setlist' # Uncomment to stop the server programmatically

"""
    run_heartbreak_code(code)
