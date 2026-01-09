# Python Errors and Exceptions

## Learning Objectives
- Understand the difference between syntax errors and exceptions
- Learn to handle exceptions with try/except blocks
- Know common exception types and their causes
- Master proper exception handling patterns

## Types of Errors

### Syntax Errors
Syntax errors (parsing errors) occur when Python can't understand your code:

```python
# Syntax Error Example
while True print('Hello world')
#                ^^^^^ SyntaxError: invalid syntax
```

The parser shows where the error was detected, but the actual mistake may be before that point. In this example, a colon (`:`) is missing before `print()`.

**Common causes of syntax errors:**
- Missing colons after `if`, `for`, `while`, `def`, `class`
- Mismatched parentheses, brackets, or braces
- Missing quotes to close strings
- Incorrect indentation
- Using Python keywords as variable names

### Exceptions
Exceptions occur during execution, even if the syntax is correct:

```python
# ZeroDivisionError
10 * (1/0)
# ZeroDivisionError: division by zero

# NameError
4 + spam*3
# NameError: name 'spam' is not defined

# TypeError
'2' + 2
# TypeError: can only concatenate str (not "int") to str
```

## Common Exception Types

| Exception | Cause |
|-----------|-------|
| `ZeroDivisionError` | Division or modulo by zero |
| `NameError` | Name not found in local or global scope |
| `TypeError` | Operation on incompatible types |
| `ValueError` | Right type but inappropriate value |
| `IndexError` | Index out of range for sequence |
| `KeyError` | Key not found in dictionary |
| `FileNotFoundError` | File or directory not found |
| `AttributeError` | Attribute reference or assignment failed |
| `IndentationError` | Incorrect indentation |
| `SyntaxError` | Parser encountered invalid syntax |

## Handling Exceptions

### Basic try/except

```python
while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("Oops! That was not a valid number. Try again...")
```

**How it works:**
1. The `try` clause is executed
2. If no exception occurs, `except` is skipped
3. If an exception occurs, the rest of `try` is skipped
4. If the exception matches the type in `except`, that block runs
5. If no match is found, the exception propagates up

### Handling Multiple Exceptions

```python
try:
    # Code that might raise exceptions
    result = some_function()
except ValueError:
    print("Invalid value!")
except TypeError:
    print("Wrong type!")
except (RuntimeError, NameError):
    # Handle multiple exceptions the same way
    print("Runtime or Name error!")
```

### Catching All Exceptions

```python
try:
    risky_operation()
except Exception as e:
    print(f"An error occurred: {e}")
```

**Warning:** Catching all exceptions can hide bugs. Be specific when possible.

### The else Clause
The `else` block runs if no exception occurred:

```python
try:
    result = int(input("Enter a number: "))
except ValueError:
    print("Invalid input!")
else:
    print(f"You entered: {result}")
    # Only runs if no exception
```

### The finally Clause
The `finally` block always runs, regardless of exceptions:

```python
try:
    file = open('example.txt', 'r')
    content = file.read()
except FileNotFoundError:
    print("File not found!")
finally:
    # This always runs - cleanup code
    if 'file' in locals():
        file.close()
```

**Better pattern using `with`:**

```python
with open('example.txt', 'r') as file:
    content = file.read()
# File automatically closed, even if exception occurs
```

## Raising Exceptions

### Using raise

```python
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return age

try:
    validate_age(-5)
except ValueError as e:
    print(f"Validation error: {e}")
```

### Re-raising Exceptions

```python
try:
    do_something()
except Exception as e:
    print(f"Error occurred: {e}")
    raise  # Re-raise the same exception
```

## Common Mistakes

### Too Broad Exception Handling

```python
# WRONG - catches everything, hides bugs
try:
    result = calculate()
except:
    pass  # Silent failure!

# CORRECT - be specific
try:
    result = calculate()
except ValueError as e:
    print(f"Calculation error: {e}")
    result = default_value
```

### Not Handling Exceptions at All

```python
# WRONG - program crashes on invalid input
age = int(input("Enter age: "))

# CORRECT - handle the error gracefully
try:
    age = int(input("Enter age: "))
except ValueError:
    print("Please enter a valid number")
    age = 0  # Or ask again
```

### Catching and Ignoring

```python
# WRONG - swallowing exceptions
try:
    risky_operation()
except Exception:
    pass

# CORRECT - at least log it
import logging

try:
    risky_operation()
except Exception as e:
    logging.error(f"Operation failed: {e}")
```

### Wrong Exception Order

```python
# WRONG - specific exception never caught
class CustomError(ValueError):
    pass

try:
    raise CustomError("Custom!")
except ValueError:
    print("ValueError")  # This catches CustomError too!
except CustomError:
    print("CustomError")  # Never reached

# CORRECT - specific exceptions first
try:
    raise CustomError("Custom!")
except CustomError:
    print("CustomError")
except ValueError:
    print("ValueError")
```

## Best Practices

1. **Be specific** - Catch only the exceptions you expect
2. **Don't silence errors** - At minimum, log them
3. **Use finally for cleanup** - Or better, use context managers (`with`)
4. **Fail fast** - Validate input early and raise meaningful exceptions
5. **Include context** - Error messages should explain what went wrong

```python
# Good exception message
def divide(a, b):
    if b == 0:
        raise ValueError(f"Cannot divide {a} by zero")
    return a / b
```

## Source
Content adapted from the official Python Tutorial: https://docs.python.org/3/tutorial/errors.html
