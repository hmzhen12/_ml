# Agent File Access Security Wrapper

A lightweight, interactive security mechanism written in Python that restricts a script or AI agent's file access. It ensures that operations are confined to the program's current working directory unless explicitly authorized by the user.

---

## Overview

When building autonomous agents or scripts that handle file paths dynamically, there is a risk of **Path Traversal** attacks (e.g., trying to access `../../../../etc/passwd` or `C:\Windows\System32`). 

This script provides a protective wrapper function, `is_safe_path()`, which evaluates if a requested file path resides safely within the program's root folder. If an agent attempts to reach outside this boundary, the script suspends the operation and prompts the human user for manual approval via the command line.

## Features

* **Automatic Sandboxing:** Automatically approves any file access requests that stay within the current working directory.
* **Interactive Safeguard:** Intercepts out-of-bound file requests and asks for explicit `y/n` user permission.
* **Path Resolution:** Uses Python's built-in `pathlib` to strictly resolve absolute paths, effectively neutralizing relative path manipulation (`../` or `./`) and symbolic link bypassing.
* **Cross-Platform Compatibility:** Works seamlessly across Windows, macOS, and Linux environments.

---

## How It Works

### 1. Path Evaluation (`is_safe_path`)
The core logic relies on the `pathlib.Path` library:
* **`base_dir`**: The script captures the current working directory where the program is running using `Path.cwd().resolve()`.
* **`target_path`**: The requested file path is converted into a strictly resolved absolute path.
* **Validation**: By calling `target_path.relative_to(base_dir)`, the script checks if the target path is a sub-directory or file within the base directory. If it throws a `ValueError`, the path is external.

### 2. Access Rules
* **Rule 1 (Internal):** If `relative_to` succeeds, the file is safely inside the program's folder. Access is immediately granted (`Returns True`).
* **Rule 2 (External):** If the file is outside, an alert `[SECURITY WARNING]` is triggered. The terminal enters a loop, asking the user to manually input `y` (allow) or `n` (deny).

---

## Example Usage

The file includes an example function, `read_file_by_agent(file_path)`, which demonstrates how to wrap your file operations using the security check.

### Allowed Operations (No Prompt)
When the agent requests files within its directory, operations execute silently and successfully:
```python
read_file_by_agent("internal_data.txt")
# Output: [SUCCESS] Successfully processed file: internal_data.txt

read_file_by_agent("./inner_folder/more_data.txt")
# Output: [SUCCESS] Successfully processed file: ./inner_folder/more_data.txt
