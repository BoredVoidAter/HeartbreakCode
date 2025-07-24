
from heartbreak_code.tokenizer import Tokenizer
from heartbreak_code.parser import Parser
from heartbreak_code.interpreter import Interpreter
from heartbreak_code.deja_vu import train_model_on_tracklist, predict_future_lyrics, analyze_sentiment_of_liner_notes
from heartbreak_code.dear_reader import execute_heartbreak_code_cell, display_tracklist_as_rich_output, display_liner_notes_as_markdown
from heartbreak_code.wasm_target import compile_to_wasm, run_wasm_module
from heartbreak_code.chart_topper import ChartTopper
from heartbreak_code.passing_notes import PassingNotes
from heartbreak_code.music_video import MusicVideo
from heartbreak_code.final_draft import FinalDraft

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

    # 'Mastermind' Structural Pattern Matching
    Speak Now: '
--- Mastermind: Structural Pattern Matching ---'
    The story of us is song_info Liner Notes are { title: 'Love Story', artist: 'Taylor Swift', year: 2008 }
    Match song_info Speak Now:
        Case Liner Notes are { title: 'Love Story', artist: 'Taylor Swift' } Speak Now:
            Speak Now: 'Matched Love Story by Taylor Swift!'
        End Case
        Case Liner Notes are { artist: 'Olivia Rodrigo', year: _ } as olivia_song Speak Now:
            Speak Now: 'Matched an Olivia Rodrigo song from year: '
            Speak Now: olivia_song.year
        End Case
        Default Speak Now:
            Speak Now: 'No match found.'
        End Case
    End Match

    The story of us is tracklist_data ['Lover', 'Fearless', 'evermore']
    Match tracklist_data Speak Now:
        Case ['Lover', _, 'evermore'] Speak Now:
            Speak Now: 'Matched a specific tracklist pattern!'
        End Case
        Default Speak Now:
            Speak Now: 'Tracklist pattern not matched.'
        End Case
    End Match

    # 'Safe & Sound' Runtime Security Sandbox
    Speak Now: '
--- Safe & Sound: Runtime Security Sandbox ---'
    Perform 'Grant Permission' Featuring permission_type='file_system_read'
    The story of us is file_exists_with_permission Does The Vault Contain 'my_secret_diary.txt'
    Speak Now: 'Does my_secret_diary.txt exist with permission?'
    Speak Now: file_exists_with_permission
    Perform 'Revoke Permission' Featuring permission_type='file_system_read'
    # This will now throw an error if uncommented:
    # The story of us is file_exists_without_permission Does The Vault Contain 'my_secret_diary.txt'
    # Speak Now: 'Does my_secret_diary.txt exist without permission?'
    # Speak Now: file_exists_without_permission

    # 'The Choreography' Build Automation and Task Runner
    Speak Now: '
--- The Choreography: Build Automation and Task Runner ---'
    Perform 'Define Choreography' Featuring name='build_project', command='echo Building project...'
    Perform 'Run Choreography' Featuring name='build_project'

    Define Verse 'MyBuildVerse': Speak Now:
        Speak Now: 'Running HeartbreakCode build verse!'
    End Verse
    Perform 'Run HeartbreakCode Choreography' Featuring verse_name='MyBuildVerse'

    # --- New Features for Version 13 ---

    # 'Déjà Vu': A Lyrical Machine Learning Framework
    Speak Now: '\n--- Déjà Vu: Lyrical Machine Learning ---'
    The story of us is tracklist_data Liner Notes are { song1: 'lyrics about love', song2: 'lyrics about breakup' }
    The story of us is lyrical_labels ['positive', 'negative']
    The story of us is trained_model Perform 'train_model_on_tracklist' Featuring tracklist_data=tracklist_data, lyrical_labels=lyrical_labels
    Speak Now: 'Trained Model: '
    Speak Now: trained_model

    The story of us is new_track Liner Notes are { song3: 'lyrics about moving on' }
    The story of us is predictions Perform 'predict_future_lyrics' Featuring trained_model=trained_model, new_track_data=new_track
    Speak Now: 'Predictions for new track: '
    Speak Now: predictions

    The story of us is liner_notes_sentiment Perform 'analyze_sentiment_of_liner_notes' Featuring liner_notes_text='This album is full of sad songs about a breakup.'
    Speak Now: 'Sentiment of liner notes: '
    Speak Now: liner_notes_sentiment

    # 'Dear Reader': Interactive Notebook Kernel
    Speak Now: '\n--- Dear Reader: Interactive Notebook Kernel ---'
    The story of us is cell_code 'Speak Now: \'Hello from a notebook cell!\''
    The story of us is cell_output Perform 'execute_heartbreak_code_cell' Featuring code_cell_content=cell_code
    Speak Now: 'Notebook Cell Output: '
    Speak Now: cell_output

    The story of us is sample_tracklist Liner Notes are { Track1: 'Verse 1', Track2: 'Chorus' }
    The story of us is rich_tracklist_output Perform 'display_tracklist_as_rich_output' Featuring tracklist_data=sample_tracklist
    Speak Now: 'Rich Tracklist Output (HTML): '
    Speak Now: rich_tracklist_output

    The story of us is sample_liner_notes '# Album Notes\n\nThis album explores themes of resilience and growth.'
    The story of us is markdown_liner_notes Perform 'display_liner_notes_as_markdown' Featuring liner_notes_content=sample_liner_notes
    Speak Now: 'Markdown Liner Notes: '
    Speak Now: markdown_liner_notes

    # 'On The World Stage': A WebAssembly Compilation Target
    Speak Now: '\n--- On The World Stage: WebAssembly Compilation ---'
    The story of us is sample_hbc_code 'Speak Now: \'Hello WASM!\''
    The story of us is wasm_output_path './output.wasm'
    The story of us is compile_result Perform 'compile_to_wasm' Featuring heartbreak_code_source=sample_hbc_code, output_path=wasm_output_path
    Speak Now: 'WASM Compilation Result: '
    Speak Now: compile_result

    Would've compile_result.status is 'success' Speak Now:
        The story of us is run_result Perform 'run_wasm_module' Featuring wasm_file_path=wasm_output_path
        Speak Now: 'WASM Run Result: '
        Speak Now: run_result
    End Verse

    # --- New Features for Version 15 ---

    # 'The Chart Topper': A Lyrical Data Visualization Library
    Speak Now: '
--- The Chart Topper: Data Visualization ---'
    The story of us is chart_data Liner Notes are { Pop: 100, Rock: 75, Indie: 50 }
    Perform 'Visualize Chart' Featuring type='bar_chart', data=chart_data, title='Genre Popularity', output_file='genre_popularity.png'

    # 'Passing Notes': A Distributed Message Queue System
    Speak Now: '
--- Passing Notes: Message Queue ---'
    Perform 'Pass Note' Featuring channel='updates', message='New album released!'
    The story of us is received_note Perform 'Listen For Note' Featuring channel='updates'
    Speak Now: 'Received Note: '
    Speak Now: received_note

    # 'The Music Video': A 2D Game and Animation Engine
    Speak Now: '
--- The Music Video: 2D Engine ---'
    Perform 'Start Music Video Engine'
    The story of us is player_sprite Perform 'Add Sprite' Featuring name='Player', position=Liner Notes are { x: 10, y: 20 }
    Perform 'Animate Sprite' Featuring sprite=player_sprite, frames=['walk1.png', 'walk2.png'], duration=0.5
    Perform 'Handle Event' Featuring event_type='keyboard', handler_verse='MyKeyboardHandler'
    Perform 'Start Game Loop'

    Define Verse 'MyKeyboardHandler' Featuring event_type, key: Speak Now:
        Speak Now: 'Keyboard event received: '
        Speak Now: event_type
        Speak Now: ' Key: '
        Speak Now: key
    End Verse

    # 'The Final Draft': A Static Analysis and Linting Tool
    Speak Now: '
--- The Final Draft: Linting Tool ---'
    The story of us is code_to_lint 'Would've my_variable is 1989 Speak Now:
    Speak Now: 'It was a good year!'
End Verse
Perform 'MyChorus'
Perform 'MyChorus'
Perform 'MyChorus'
Perform 'MyChorus'
Perform 'MyChorus'
Perform 'MyChorus''
    The story of us is linting_report Perform 'Analyze Code' Featuring code=code_to_lint
    Speak Now: 'Linting Report: '
    Speak Now: linting_report

"""


