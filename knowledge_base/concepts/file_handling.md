# Python File Handling

## Learning Objectives
- Understand how to open, read, and write files
- Master the `with` statement for safe file handling
- Learn different file modes and their purposes
- Handle file-related errors properly

## Opening Files

### Using the with Statement (Recommended)
The `with` statement ensures files are properly closed:

```python
with open("example.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
# File is automatically closed here, even if an error occurred
```

### File Modes
| Mode | Description |
|------|-------------|
| `"r"` | Read only (default). File must exist. |
| `"w"` | Write only. Creates new file or **overwrites** existing! |
| `"a"` | Append. Adds to end of file. Creates if doesn't exist. |
| `"x"` | Exclusive creation. Fails if file exists. |
| `"r+"` | Read and write. File must exist. |
| `"w+"` | Write and read. Creates new or **overwrites**. |
| `"b"` | Binary mode (add to other mode, e.g., `"rb"`). |

## Reading Files

### Read Entire File
```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()  # Returns entire file as one string
    print(content)
```

### Read Line by Line
```python
# Method 1: readline() - one line at a time
with open("data.txt", "r", encoding="utf-8") as f:
    line = f.readline()  # First line
    line2 = f.readline() # Second line

# Method 2: readlines() - all lines as a list
with open("data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()  # ["line1\n", "line2\n", ...]

# Method 3: Iterate (Best for large files)
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())  # strip() removes trailing newline
```

### Reading with Context
```python
# Read first 100 characters
with open("data.txt", "r", encoding="utf-8") as f:
    chunk = f.read(100)

# Seek to a position
with open("data.txt", "r", encoding="utf-8") as f:
    f.seek(10)  # Move to byte position 10
    remaining = f.read()
```

## Writing Files

### Write Text
```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("Second line\n")
```

### Write Multiple Lines
```python
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]

with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)  # Writes all lines at once
```

### Append to File
```python
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New log entry\n")  # Added to end, existing content preserved
```

## Common Mistakes

### Forgetting to Close Files
Without `with`, you must close manually:

```python
# WRONG - file might not close on error
f = open("data.txt", "r")
content = f.read()
# If error happens here, file stays open!
f.close()

# CORRECT - use 'with' for automatic closing
with open("data.txt", "r") as f:
    content = f.read()
# File automatically closed, even if error occurs
```

### Using "w" Mode Accidentally
Write mode completely erases the file first:

```python
# DANGER! This erases all existing content:
with open("important_data.txt", "w") as f:
    f.write("New content")  # Old content is GONE

# Use "a" to append instead:
with open("log.txt", "a") as f:
    f.write("Added to end\n")
```

### FileNotFoundError
Always handle the case when file doesn't exist:

```python
# WRONG - crashes if file missing
with open("missing.txt", "r") as f:
    content = f.read()  # FileNotFoundError!

# CORRECT - handle the error
try:
    with open("missing.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found!")
    content = ""
```

### Encoding Issues
Mixing encodings causes garbled text or errors:

```python
# WRONG - may fail with non-ASCII characters
with open("data.txt", "r") as f:
    content = f.read()  # UnicodeDecodeError possible

# CORRECT - always specify encoding
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### Reading Large Files into Memory
Don't load huge files all at once:

```python
# WRONG for large files
with open("huge_file.txt", "r") as f:
    content = f.read()  # Could use gigabytes of RAM!

# CORRECT - process line by line
with open("huge_file.txt", "r") as f:
    for line in f:
        process(line)  # Only one line in memory
```

## Checking if File Exists

```python
import os

if os.path.exists("data.txt"):
    with open("data.txt", "r") as f:
        content = f.read()
else:
    print("File does not exist")

# Or use pathlib (more modern)
from pathlib import Path

if Path("data.txt").exists():
    content = Path("data.txt").read_text()
```

## Working with File Paths

```python
import os
from pathlib import Path

# Using os.path (traditional)
folder = "documents"
filename = "report.txt"
full_path = os.path.join(folder, filename)  # "documents/report.txt"

# Using pathlib (modern, recommended)
path = Path("documents") / "report.txt"
print(path.exists())
print(path.read_text())  # Shortcut for opening and reading
```

## Binary Files

```python
# Reading binary (images, etc.)
with open("image.png", "rb") as f:
    data = f.read()

# Writing binary
with open("copy.png", "wb") as f:
    f.write(data)
```

## Source
Based on Python Tutorial: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
