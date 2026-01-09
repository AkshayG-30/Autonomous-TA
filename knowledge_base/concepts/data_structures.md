# Python Data Structures

## Learning Objectives
- Master Python's built-in data structures: lists, dictionaries, tuples, and sets
- Understand when to use each data structure
- Learn common operations and methods for each type

## Lists

### List Basics
Lists are ordered, mutable sequences:

```python
fruits = ['apple', 'banana', 'cherry']
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
```

### List Methods

```python
fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']

# Count occurrences
fruits.count('apple')   # 2
fruits.count('tangerine')  # 0

# Find index
fruits.index('banana')  # 3
fruits.index('banana', 4)  # 6 (search starting at position 4)

# Modify list
fruits.reverse()        # Reverses in place
fruits.append('grape')  # Add to end
fruits.sort()           # Sort in place
fruits.pop()            # Remove and return last item -> 'pear'
```

**Key List Methods:**
| Method | Description |
|--------|-------------|
| `append(x)` | Add item to end |
| `extend(iterable)` | Add all items from iterable |
| `insert(i, x)` | Insert item at position i |
| `remove(x)` | Remove first occurrence of x |
| `pop([i])` | Remove and return item at position i (default: last) |
| `clear()` | Remove all items |
| `index(x)` | Return index of first x |
| `count(x)` | Count occurrences of x |
| `sort()` | Sort in place |
| `reverse()` | Reverse in place |
| `copy()` | Return shallow copy |

### List Comprehensions
Concise way to create lists:

```python
# Create list of squares
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Nested comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Using Lists as Stacks
Use `append()` and `pop()` for LIFO (Last In, First Out):

```python
stack = [3, 4, 5]
stack.append(6)    # [3, 4, 5, 6]
stack.append(7)    # [3, 4, 5, 6, 7]
stack.pop()        # Returns 7, stack is now [3, 4, 5, 6]
```

## Dictionaries

### Dictionary Basics
Dictionaries store key-value pairs:

```python
tel = {'jack': 4098, 'sape': 4139}
tel['guido'] = 4127  # Add new entry
print(tel['jack'])   # 4098
del tel['sape']      # Delete entry
```

**Key Points:**
- Keys must be immutable (strings, numbers, tuples of immutables)
- Keys must be unique within a dictionary
- Accessing a non-existent key raises `KeyError`

### Safe Key Access
Use `get()` to avoid KeyError:

```python
tel = {'jack': 4098, 'guido': 4127}

# This raises KeyError
# print(tel['irv'])

# Use get() for safe access
print(tel.get('irv'))          # None
print(tel.get('irv', 'N/A'))   # 'N/A' (default value)
```

### Dictionary Operations

```python
tel = {'jack': 4098, 'sape': 4139, 'guido': 4127}

# Check membership
'guido' in tel      # True
'jack' not in tel   # False

# Get all keys/values
list(tel)           # ['jack', 'sape', 'guido']
sorted(tel)         # ['guido', 'jack', 'sape']
list(tel.values())  # [4098, 4139, 4127]
list(tel.items())   # [('jack', 4098), ('sape', 4139), ('guido', 4127)]
```

### Dictionary Comprehensions

```python
# Create squares dictionary
squares = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

## Tuples

### Tuple Basics
Tuples are immutable sequences:

```python
# Create tuples
t = (1, 2, 3)
single = (42,)  # Note the comma for single-element tuple
empty = ()

# Tuple packing and unpacking
coordinates = 12345, 54321, 'hello'  # Packing
x, y, z = coordinates               # Unpacking
```

**When to use tuples vs lists:**
- Use tuples for heterogeneous data (like database records)
- Use lists for homogeneous data (items of the same type)
- Use tuples when you need immutability (e.g., as dictionary keys)

## Sets

### Set Basics
Sets are unordered collections of unique elements:

```python
# Create sets
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print(basket)  # {'orange', 'banana', 'pear', 'apple'} - duplicates removed

# From string
letters = set('abracadabra')
# {'a', 'r', 'b', 'c', 'd'}
```

### Set Operations

```python
a = set('abracadabra')  # {'a', 'r', 'b', 'c', 'd'}
b = set('alacazam')     # {'a', 'l', 'c', 'z', 'm'}

a - b   # Difference: {'r', 'd', 'b'}
a | b   # Union: {'a', 'c', 'r', 'd', 'b', 'm', 'z', 'l'}
a & b   # Intersection: {'a', 'c'}
a ^ b   # Symmetric difference: {'r', 'd', 'b', 'm', 'z', 'l'}
```

### Set Comprehensions

```python
# Create set of squares
squares = {x**2 for x in range(10)}
# {0, 1, 64, 4, 36, 9, 16, 49, 81, 25}
```

## Looping Techniques

### Loop with Index

```python
# Using enumerate
for i, value in enumerate(['a', 'b', 'c']):
    print(i, value)
```

### Loop Over Dictionary

```python
knights = {'gallahad': 'the pure', 'robin': 'the brave'}

for key, value in knights.items():
    print(key, value)
```

### Loop Over Two Sequences

```python
questions = ['name', 'quest', 'color']
answers = ['lancelot', 'the holy grail', 'blue']

for q, a in zip(questions, answers):
    print(f'What is your {q}? It is {a}.')
```

## Common Mistakes

### Modifying List While Iterating

```python
# WRONG - unpredictable behavior
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)

# CORRECT - iterate over a copy
numbers = [1, 2, 3, 4, 5]
for n in numbers.copy():
    if n % 2 == 0:
        numbers.remove(n)
```

### Using List as Dictionary Key

```python
# WRONG - lists are mutable, can't be keys
# my_dict = {[1, 2]: "value"}  # TypeError

# CORRECT - use tuple instead
my_dict = {(1, 2): "value"}
```

### KeyError When Accessing Dictionary

```python
# WRONG - raises KeyError if key doesn't exist
# value = my_dict['nonexistent']

# CORRECT - use get() with default
value = my_dict.get('nonexistent', 'default_value')

# Or check first
if 'key' in my_dict:
    value = my_dict['key']
```

## Source
Content adapted from the official Python Tutorial: https://docs.python.org/3/tutorial/datastructures.html
