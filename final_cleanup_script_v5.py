
import os

file_to_delete = "C:/Users/finni/Desktop/Projects/HeartbreakCode/final_cleanup_script_v4.py"
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"Successfully deleted {file_to_delete}")
else:
    print(f"File not found: {file_to_delete}")
