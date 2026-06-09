import os
from pathlib import Path

def is_safe_path(target_path_str):
    """
    Function to check if the file is located inside the program's folder.
    If it is outside, it will prompt the user for approval.
    """
    base_dir = Path.cwd().resolve()
   
    target_path = Path(target_path_str).resolve()
  
    try:
        target_path.relative_to(base_dir)
        is_internal = True
    except ValueError:
        is_internal = False

    if is_internal:
        return True
    else:
        print(f"\n[SECURITY WARNING] The agent is attempting to access a file outside the program directory!")
        print(f"Target File: {target_path}")
        
        while True:
            approval = input("Do you allow this access? (y/n): ").strip().lower()
            if approval == 'y':
                print("[INFO] Access granted by the user.")
                return True
            elif approval == 'n':
                print("[INFO] Access denied by the user.")
                return False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

def read_file_by_agent(file_path):
    print(f"\n--> Agent wants to read: {file_path}")
    
    if is_safe_path(file_path):
        try:
            print(f"[SUCCESS] Successfully processed file: {file_path}")
        except FileNotFoundError:
            print(f"[ERROR] File not found.")
    else:
        print("[FAILED] Operation aborted due to security reasons.")

if __name__ == "__main__":
    read_file_by_agent("internal_data.txt")
    read_file_by_agent("./inner_folder/more_data.txt")
    
    # Adjust the paths below according to your OS (examples for Windows/Linux)
    read_file_by_agent("../secret.txt") 
    read_file_by_agent("/etc/passwd") 
