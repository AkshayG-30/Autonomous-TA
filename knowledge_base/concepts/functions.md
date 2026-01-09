# Python Functions

## Learning Objectives
- Understand how to define functions using `def`
- Learn about function parameters and return values
- Master docstrings for documentation
- Understand variable scope in functions

## Defining Functions

### Basic Function Definition
Use the `def` keyword to define a function:

```python
def fib(n):
    """Print a Fibonacci series less than n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()

# Call the function
fib(2000)
# Output: 0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597
```

**Key Components:**
1. The `def` keyword introduces a function definition
2. Function name followed by parenthesized parameters
3. Function body starts on the next line and must be indented
4. The first statement can be a docstring (documentation string)

### Return Values
Functions can return values using the `return` statement:

```python
def fib2(n):
    """Return a list containing the Fibonacci series up to n."""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result

f100 = fib2(100)
print(f100)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```

**Key Points:**
- `return` without an expression returns `None`
- Falling off the end of a function also returns `None`
- Even functions without a `return` statement return `None`

```python
def no_return():
    pass

result = no_return()
print(result)  # None
```

## Function Parameters

### Default Argument Values
You can specify default values for parameters:

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")           # Hello, Alice!
greet("Bob", "Hi")       # Hi, Bob!
```

### Keyword Arguments
Call functions using keyword arguments for clarity:

```python
def describe_pet(animal, name, age=1):
    print(f"{name} is a {animal}, {age} year(s) old")

# All these work:
describe_pet("cat", "Whiskers")
describe_pet(animal="dog", name="Buddy", age=3)
describe_pet("hamster", name="Squeaky", age=2)
```

### Arbitrary Arguments (*args and **kwargs)
Accept variable numbers of arguments:

```python
# *args for positional arguments
def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3, 4))  # 10

# **kwargs for keyword arguments
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="NYC")
```

## Documentation Strings (Docstrings)

### Writing Good Docstrings
The first statement of a function can be a documentation string:

```python
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.
    
    Args:
        length: The length of the rectangle (must be positive)
        width: The width of the rectangle (must be positive)
    
    Returns:
        The area as a float
    
    Raises:
        ValueError: If length or width is negative
    """
    if length < 0 or width < 0:
        raise ValueError("Dimensions must be positive")
    return length * width
```

**Best Practices:**
- First line: brief summary of the function's purpose
- Leave a blank line before the detailed description
- Document parameters, return values, and exceptions
- Access docstring via `function.__doc__`

## Variable Scope

### Local vs Global Variables
Variables inside functions are local by default:

```python
x = 10  # Global variable

def my_function():
    x = 5  # Local variable (different from global x)
    print(f"Inside function: x = {x}")

my_function()
print(f"Outside function: x = {x}")
# Output:
# Inside function: x = 5
# Outside function: x = 10
```

### Using global and nonlocal
To modify global variables, use the `global` keyword:

```python
count = 0

def increment():
    global count
    count += 1

increment()
print(count)  # 1
```

For nested functions, use `nonlocal`:

```python
def outer():
    x = 10
    
    def inner():
        nonlocal x
        x += 1
    
    inner()
    print(x)  # 11

outer()
```

## Common Mistakes

### Mutable Default Arguments
Never use mutable objects as default arguments:

```python
# WRONG - the list persists between calls!
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("apple"))   # ['apple']
print(add_item("banana"))  # ['apple', 'banana'] - unexpected!

# CORRECT - use None and create new list
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Forgetting to Return
If you need a value from a function, explicitly return it:

```python
# WRONG - returns None
def double(x):
    result = x * 2  # Forgot to return!

# CORRECT
def double(x):
    return x * 2
```

## Source
Content adapted from the official Python Tutorial: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
