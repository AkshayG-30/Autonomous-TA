# Python Input and Output

## Learning Objectives
- Understand how to get user input with `input()`
- Master output formatting with `print()` and f-strings
- Learn type conversion for user input
- Avoid common input/output mistakes

## The input() Function

### Basic Usage
The `input()` function reads a line of text from the user:

```python
name = input("Enter your name: ")
print(f"Hello, {name}!")
```

**Key Point:** `input()` always returns a **string**, even if the user types a number!

### Converting Input Types
Convert input to other types as needed:

```python
# Get a number from user
age = int(input("Enter your age: "))
print(f"In 10 years, you'll be {age + 10}")

# Get a decimal number
price = float(input("Enter the price: "))
print(f"With tax: ${price * 1.1:.2f}")
```

## The print() Function

### Basic Printing
```python
print("Hello, World!")
print("Multiple", "values", "separated")  # Prints with spaces
print()  # Prints empty line
```

### Print Parameters
```python
# sep: separator between values (default: space)
print("a", "b", "c", sep="-")  # "a-b-c"

# end: string appended after last value (default: newline)
print("Loading", end="")
print("...")  # "Loading..." on same line
```

## String Formatting

### f-strings (Recommended)
The most modern and readable way to format strings:

```python
name = "Alice"
age = 25
score = 85.5

# Basic usage
print(f"Name: {name}, Age: {age}")

# Expressions inside braces
print(f"Next year: {age + 1}")

# Formatting numbers
print(f"Score: {score:.1f}")      # One decimal: 85.5
print(f"Score: {score:.0f}%")     # No decimals: 86%
print(f"Number: {42:05d}")        # Pad with zeros: 00042
print(f"Price: ${9.99:>10.2f}")   # Right-align, width 10
```

### Common Format Specifications
| Format | Description | Example |
|--------|-------------|---------|
| `:.2f` | 2 decimal places | `3.14` |
| `:05d` | Pad integer with zeros | `00042` |
| `:>10` | Right-align, width 10 | `     hello` |
| `:<10` | Left-align, width 10 | `hello     ` |
| `:^10` | Center, width 10 | `  hello   ` |
| `:,` | Add commas | `1,000,000` |
| `:.2%` | Percentage | `75.00%` |

### Using .format() Method
Older but still valid approach:

```python
print("Hello, {}!".format(name))
print("Name: {0}, Age: {1}".format(name, age))
print("Name: {n}, Age: {a}".format(n=name, a=age))
```

## Common Mistakes

### Forgetting Type Conversion
`input()` returns a string, even for numbers:

```python
# WRONG - tries to add string and int
age = input("Enter age: ")
new_age = age + 1  # TypeError!

# CORRECT - convert to int first
age = int(input("Enter age: "))
new_age = age + 1
```

### Not Handling Invalid Input
Users might enter unexpected values:

```python
# WRONG - crashes on non-numeric input
age = int(input("Enter age: "))  # ValueError if user types "abc"

# CORRECT - handle the error
try:
    age = int(input("Enter age: "))
except ValueError:
    print("Please enter a valid number")
    age = 0
```

### Concatenating Strings and Numbers
You can't directly concatenate different types:

```python
age = 25

# WRONG
print("Age: " + age)  # TypeError!

# CORRECT - convert to string
print("Age: " + str(age))

# BETTER - use f-string (automatic conversion)
print(f"Age: {age}")
```

### Empty Input
Handle the case when user presses Enter without typing:

```python
name = input("Enter name (or press Enter to skip): ")
if name:
    print(f"Hello, {name}!")
else:
    print("No name provided")
```

## Input Validation Pattern

```python
def get_positive_number(prompt):
    """Keep asking until user enters a valid positive number."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive number")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Usage
age = get_positive_number("Enter your age: ")
```

## Source
Based on Python Tutorial: https://docs.python.org/3/tutorial/inputoutput.html
