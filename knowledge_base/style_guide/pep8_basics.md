# PEP 8 Style Guide Basics

## Learning Objectives
- Understand Python's official style conventions
- Learn proper indentation and whitespace usage
- Master naming conventions for variables, functions, and classes
- Write clean, readable, professional Python code

## Why Style Matters

Good code style makes your code:
- **Readable** - Others (and future you) can understand it quickly
- **Consistent** - Follows patterns that Python developers expect
- **Professional** - Shows attention to detail and craftsmanship

## Indentation

### Use 4 Spaces Per Indentation Level

```python
# CORRECT - 4 spaces
def my_function():
    if condition:
        do_something()
        do_something_else()

# WRONG - 2 spaces
def my_function():
  if condition:
    do_something()
```

**Key Rules:**
- Use spaces, not tabs
- Python 3 disallows mixing tabs and spaces
- Most editors can convert Tab key to 4 spaces automatically

### Continuation Lines

```python
# CORRECT - Aligned with opening delimiter
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# CORRECT - Hanging indent with extra level
def long_function_name(
        var_one, var_two,
        var_three, var_four):
    print(var_one)

# WRONG - Arguments on first line without alignment
foo = long_function_name(var_one, var_two,
    var_three, var_four)
```

## Maximum Line Length

- **Limit lines to 79 characters** for code
- **Limit to 72 characters** for docstrings and comments
- Use implied line continuation inside parentheses, brackets, or braces

```python
# Line continuation with parentheses
if (this_is_one_thing
        and that_is_another_thing):
    do_something()

# Line continuation with backslash (less preferred)
total = first_value + \
        second_value + \
        third_value
```

## Blank Lines

- **Two blank lines** around top-level functions and classes
- **One blank line** between method definitions inside a class
- Use blank lines sparingly inside functions to indicate logical sections

```python
class MyClass:
    """Class docstring."""
    
    def method_one(self):
        pass
    
    def method_two(self):
        pass


def standalone_function():
    pass


def another_function():
    pass
```

## Naming Conventions

### Variables and Functions
Use `lowercase_with_underscores` (snake_case):

```python
# CORRECT
user_name = "Alice"
student_count = 42

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# WRONG
userName = "Alice"      # camelCase
StudentCount = 42       # PascalCase
calculateAverage = ...  # camelCase
```

### Classes
Use `CapitalizedWords` (PascalCase):

```python
# CORRECT
class StudentRecord:
    pass

class HTTPConnection:
    pass

# WRONG
class student_record:
    pass

class httpConnection:
    pass
```

### Constants
Use `ALL_CAPS_WITH_UNDERSCORES`:

```python
# CORRECT
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
PI = 3.14159

# WRONG
maxConnections = 100
default_timeout = 30
```

### Private Variables
Use a leading underscore for private attributes:

```python
class MyClass:
    def __init__(self):
        self.public_var = "visible"
        self._private_var = "internal use"
        self.__mangled_var = "name mangled"
```

## Whitespace

### Around Operators

```python
# CORRECT
x = 1
y = x + 1
result = (a + b) * (c - d)

# WRONG
x=1
y = x+1
result = (a+b)*(c-d)
```

### No Space Inside Brackets

```python
# CORRECT
spam(ham[1], {eggs: 2})

# WRONG
spam( ham[ 1 ], { eggs: 2 } )
```

### After Commas

```python
# CORRECT
x, y = 1, 2
my_list = [1, 2, 3]
my_dict = {'a': 1, 'b': 2}

# WRONG
x,y = 1,2
my_list = [1,2,3]
```

### No Space Before Colon in Slices

```python
# CORRECT
my_list[1:3]
my_list[::2]

# WRONG
my_list[1 : 3]
my_list[ : : 2]
```

## Imports

### Import Order
1. Standard library imports
2. Related third-party imports
3. Local application imports

Separate each group with a blank line.

```python
# CORRECT
import os
import sys

import numpy as np
import pandas as pd

from my_package import my_module
```

### One Import Per Line

```python
# CORRECT
import os
import sys

# WRONG
import os, sys
```

### From Imports on Same Line is OK

```python
# CORRECT
from subprocess import Popen, PIPE
```

## Comments

### Block Comments
Start each line with `#` and a space:

```python
# This is a block comment explaining
# the following code section.
# It can span multiple lines.
```

### Inline Comments
Separate from code by at least two spaces:

```python
x = x + 1  # Increment counter
```

### Docstrings
Use triple quotes for documentation:

```python
def complex_function(param1, param2):
    """
    Brief description of the function.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
    
    Returns:
        Description of return value
    """
    pass
```

## Common Style Mistakes

### Inconsistent Naming

```python
# WRONG - mixing styles
userName = "Alice"      # camelCase
user_age = 25           # snake_case
UserCity = "NYC"        # PascalCase

# CORRECT - consistent snake_case
user_name = "Alice"
user_age = 25
user_city = "NYC"
```

### Too Long Lines

```python
# WRONG - exceeds 79 characters
result = some_function(first_argument, second_argument, third_argument, fourth_argument, fifth_argument)

# CORRECT - split across lines
result = some_function(
    first_argument,
    second_argument,
    third_argument,
    fourth_argument,
    fifth_argument
)
```

### Missing Whitespace

```python
# WRONG
x=y+z
if(condition):
    do_something(a,b,c)

# CORRECT
x = y + z
if condition:
    do_something(a, b, c)
```

## Grading Criteria for Code Style

When grading for style, look for:
- **Proper indentation** (4 spaces): 30%
- **Meaningful variable names**: 30%
- **Consistent naming conventions**: 20%
- **Appropriate whitespace**: 10%
- **Clear comments where needed**: 10%

## Source
Content adapted from PEP 8: https://peps.python.org/pep-0008/
