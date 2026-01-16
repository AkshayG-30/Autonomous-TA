# Lab 2: Introduction to Python Functions

## Learning Objectives
- Understand how to define functions using `def`
- Learn about parameters, arguments, and return values
- Practice creating reusable code blocks
- Avoid common function-related mistakes

## Instructions

### Task 1: Basic Calculator Functions
Create a simple calculator with separate functions for each operation.

Requirements:
1. Create functions `add(a, b)`, `subtract(a, b)`, `multiply(a, b)`, and `divide(a, b)`
2. Each function should take two numbers and return the result
3. The `divide` function should handle division by zero (print an error message and return `None`)

Example usage:
```python
print(add(5, 3))       # Should print: 8
print(divide(10, 2))   # Should print: 5.0
print(divide(10, 0))   # Should print error message
```

### Task 2: Temperature Converter
Write functions to convert between Celsius and Fahrenheit.

Requirements:
1. Create `celsius_to_fahrenheit(celsius)` - uses formula: F = C × 9/5 + 32
2. Create `fahrenheit_to_celsius(fahrenheit)` - uses formula: C = (F - 32) × 5/9
3. Both functions should return the converted value rounded to 2 decimal places
4. Add docstrings to explain what each function does

### Task 3: Greeting Function with Default Parameter
Create a function that greets a user with a customizable greeting.

Requirements:
1. Create `greet(name, greeting="Hello")` with a default parameter
2. The function should return the greeting string (not print it)
3. Test with both default and custom greetings

Example:
```python
print(greet("Alice"))           # "Hello, Alice!"
print(greet("Bob", "Hi"))       # "Hi, Bob!"
```

## Common Mistakes

### Forgetting to Return a Value
If you need to use a function's result, you must explicitly return it:

```python
# WRONG - this returns None
def double(x):
    result = x * 2  # Calculated but not returned!

# CORRECT
def double(x):
    return x * 2
```

### Mutable Default Arguments
Never use mutable objects (lists, dicts) as default arguments:

```python
# WRONG - the list persists between calls!
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("apple"))   # ['apple']
print(add_item("banana"))  # ['apple', 'banana'] - unexpected!

# CORRECT - use None and create new list inside
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Printing Instead of Returning
Functions that print don't give you a value to work with:

```python
# WRONG - can't use the result
def calculate_sum(a, b):
    print(a + b)

result = calculate_sum(5, 3)
print(result * 2)  # Error! result is None

# CORRECT - return the value
def calculate_sum(a, b):
    return a + b

result = calculate_sum(5, 3)
print(result * 2)  # Works! Prints 16
```

### Forgetting Parentheses When Calling
A function name without parentheses is a reference, not a call:

```python
def say_hello():
    return "Hello!"

# WRONG - this is the function object, not the result
message = say_hello
print(message)  # Prints: <function say_hello at 0x...>

# CORRECT - call with parentheses
message = say_hello()
print(message)  # Prints: Hello!
```

## Grading Criteria
- Functions work correctly with various inputs: 40%
- Proper use of return statements: 20%
- Docstrings included: 15%
- Handles edge cases (division by zero): 15%
- Code style (proper naming, indentation): 10%

## Source
Based on Python Tutorial: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
