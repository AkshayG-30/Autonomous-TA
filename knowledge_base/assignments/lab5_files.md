# Lab 5: File Input/Output in Python

## Learning Objectives
- Understand how to open, read, and write files
- Master the `with` statement for safe file handling
- Learn different file modes (read, write, append)
- Handle file-related errors gracefully

## Instructions

### Task 1: Reading a Text File
Read and process content from a text file.

Requirements:
1. Create a file called `students.txt` with this content:
   ```
   Alice,85
   Bob,92
   Charlie,78
   Diana,90
   ```
2. Read the file and parse each line
3. Calculate the average grade
4. Print each student's name and whether they're above or below average

### Task 2: Writing to a File
Create a program that writes a report to a file.

Requirements:
1. Create a list of items: `["apple", "banana", "cherry", "date"]`
2. Write each item to a file called `shopping_list.txt`, one per line
3. Add line numbers: "1. apple", "2. banana", etc.
4. Read the file back and print its contents to verify

### Task 3: Appending to a File
Add new entries to an existing file without overwriting.

Requirements:
1. Start with the shopping list from Task 2
2. Append 3 new items to the file
3. Read and display the complete list

### Task 4: CSV Processing (Advanced)
Work with comma-separated data.

Requirements:
1. Read `students.txt` from Task 1
2. Add 10 bonus points to each student's grade
3. Write the updated data to `students_updated.txt`
4. Handle the case where the input file doesn't exist

## Common Mistakes

### Forgetting to Close Files
Always close files after use, or better, use `with`:

```python
# WRONG - file might stay open if error occurs
file = open("data.txt", "r")
content = file.read()
# If error happens here, file never closes!
file.close()

# CORRECT - 'with' automatically closes the file
with open("data.txt", "r") as file:
    content = file.read()
# File is automatically closed here, even if error occurs
```

### Wrong File Mode
Using the wrong mode can lose data or fail:

```python
# Common modes:
# "r"  - read only (default), file must exist
# "w"  - write only, CREATES NEW or OVERWRITES existing!
# "a"  - append, adds to end of file
# "r+" - read and write

# WRONG - "w" erases everything!
with open("important_data.txt", "w") as f:
    # The file is now EMPTY, all previous content is gone!
    pass

# CORRECT - use "a" to add without erasing
with open("log.txt", "a") as f:
    f.write("New log entry\n")
```

### FileNotFoundError
Handle missing files gracefully:

```python
# WRONG - crashes if file doesn't exist
with open("missing.txt", "r") as f:
    content = f.read()  # FileNotFoundError!

# CORRECT - handle the error
try:
    with open("missing.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found! Creating a new one...")
    content = ""
```

### Encoding Issues
Specify encoding for non-ASCII characters:

```python
# WRONG - may fail with special characters on some systems
with open("data.txt", "r") as f:
    content = f.read()

# CORRECT - always specify encoding
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### Reading Large Files All at Once
Don't load huge files into memory:

```python
# WRONG for large files - loads entire file into memory
with open("huge_file.txt", "r") as f:
    all_content = f.read()  # Could use gigabytes of RAM!

# CORRECT - process line by line
with open("huge_file.txt", "r") as f:
    for line in f:
        process_line(line)  # Only one line in memory at a time
```

## File Reading Methods

```python
with open("example.txt", "r", encoding="utf-8") as f:
    # Read entire file as string
    content = f.read()
    
    # Read one line at a time
    line = f.readline()
    
    # Read all lines into a list
    lines = f.readlines()
    
    # Best: iterate line by line
    for line in f:
        print(line.strip())  # strip() removes newline
```

## File Writing Methods

```python
with open("output.txt", "w", encoding="utf-8") as f:
    # Write a string
    f.write("Hello, World!\n")
    
    # Write multiple lines
    lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
    f.writelines(lines)
```

## Grading Criteria
- Correct use of `with` statement: 25%
- Files read and written correctly: 30%
- Error handling (FileNotFoundError): 20%
- Proper encoding specified: 10%
- Code style and documentation: 15%

## Source
Based on Python Tutorial: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
