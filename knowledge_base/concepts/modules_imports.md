# Python Modules and Imports

## Learning Objectives
- Understand what modules are and why they're useful
- Learn different import statements and when to use each
- Work with common standard library modules
- Avoid common import-related mistakes

## What is a Module?

A module is a file containing Python code (definitions and statements). Modules let you organize code into reusable files.

```python
# Example: a module named 'mymath.py'
# mymath.py
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

PI = 3.14159
```

## Import Statements

### Basic Import
Import the entire module:

```python
import math

# Access with module.name
print(math.sqrt(16))    # 4.0
print(math.pi)          # 3.141592653589793
```

### Import with Alias
Give the module a shorter name:

```python
import numpy as np
import pandas as pd

array = np.array([1, 2, 3])
```

### Import Specific Items
Import only what you need:

```python
from math import sqrt, pi

# Use directly without module prefix
print(sqrt(16))  # 4.0
print(pi)        # 3.141592653589793
```

### Import Everything (Avoid!)
Imports all names from a module:

```python
from math import *

# Now you can use all math functions without prefix
# BUT this is discouraged! See "Common Mistakes" section
```

## Common Standard Library Modules

### math - Mathematical Functions
```python
import math

math.sqrt(16)        # 4.0 - square root
math.pow(2, 3)       # 8.0 - power
math.floor(3.7)      # 3 - round down
math.ceil(3.2)       # 4 - round up
math.pi              # 3.141592... - constant
```

### random - Random Numbers
```python
import random

random.random()              # Random float 0.0 to 1.0
random.randint(1, 10)        # Random int from 1 to 10 (inclusive)
random.choice(['a', 'b'])    # Random item from list
random.shuffle(my_list)      # Shuffle list in place
```

### os - Operating System Interface
```python
import os

os.getcwd()                  # Current working directory
os.listdir('.')              # List directory contents
os.path.exists('file.txt')   # Check if file exists
os.path.join('folder', 'file.txt')  # Build paths safely
```

### datetime - Date and Time
```python
from datetime import datetime, date

now = datetime.now()         # Current date and time
today = date.today()         # Current date
print(now.strftime("%Y-%m-%d"))  # Format as string
```

## Common Mistakes

### Shadowing Module Names
Don't name your file the same as a module you're importing:

```python
# WRONG - if your file is named 'random.py'
import random
print(random.randint(1, 10))  # Error! It imports YOUR file, not the standard library

# CORRECT - name your file something else like 'my_random_test.py'
```

### Using "from module import *"
This pollutes your namespace and causes confusion:

```python
# WRONG - where does sqrt come from?
from math import *
from numpy import *

result = sqrt(16)  # Which sqrt? math or numpy?

# CORRECT - be explicit
from math import sqrt
from numpy import array

# Or use the module prefix
import math
import numpy as np

result = math.sqrt(16)
```

### Circular Imports
Two modules importing each other causes problems:

```python
# file_a.py
from file_b import function_b
def function_a():
    return function_b()

# file_b.py
from file_a import function_a  # Error! Circular import
def function_b():
    return function_a()

# SOLUTION: Restructure your code to avoid the circular dependency
# Or move the import inside the function that needs it
```

### Import Order Convention
Follow PEP 8 import ordering:

```python
# CORRECT order:
# 1. Standard library imports
import os
import sys

# 2. Third-party imports
import numpy as np
import pandas as pd

# 3. Local application imports
from mypackage import mymodule
```

## Checking Module Contents

Use `dir()` to see what's in a module:

```python
import math

print(dir(math))
# ['acos', 'acosh', 'asin', 'asinh', 'atan', 'ceil', 'cos', ...]

# Get help on a specific function
help(math.sqrt)
```

## if __name__ == "__main__"

This pattern lets a file work as both a module and a script:

```python
# mymodule.py
def main():
    print("Running as a script!")

if __name__ == "__main__":
    # Only runs when this file is executed directly
    # Not when imported as a module
    main()
```

## Source
Based on Python Tutorial: https://docs.python.org/3/tutorial/modules.html
