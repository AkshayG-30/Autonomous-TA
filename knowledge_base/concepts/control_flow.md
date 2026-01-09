# Python Control Flow

## Learning Objectives
- Understand how to use `if`, `elif`, and `else` statements for conditional execution
- Master `for` and `while` loops for iteration
- Learn to use `range()` for generating sequences of numbers
- Understand `break` and `continue` statements for loop control

## Conditional Statements

### The if Statement
The `if` statement is used for conditional execution:

```python
x = int(input("Please enter an integer: "))
if x < 0:
    x = 0
    print('Negative changed to zero')
elif x == 0:
    print('Zero')
elif x == 1:
    print('Single')
else:
    print('More')
```

**Key Points:**
- There can be zero or more `elif` parts
- The `else` part is optional
- The keyword `elif` is short for "else if" and helps avoid excessive indentation
- An `if...elif...elif...` sequence is a substitute for `switch` or `case` statements in other languages

## Loops

### The for Statement
Python's `for` statement iterates over items of any sequence (list, string, etc.):

```python
# Measure some strings
words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))
# Output:
# cat 3
# window 6
# defenestrate 12
```

**Important:** Don't modify a collection while iterating over it. Instead, loop over a copy or create a new collection:

```python
users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

# Strategy 1: Iterate over a copy
for user, status in users.copy().items():
    if status == 'inactive':
        del users[user]

# Strategy 2: Create a new collection
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status
```

### The range() Function
The `range()` function generates arithmetic progressions for iteration:

```python
for i in range(5):
    print(i)
# Output: 0, 1, 2, 3, 4
```

**Key Points about range():**
- The end point is never included: `range(10)` generates 0 through 9
- You can specify a start: `range(5, 10)` generates 5, 6, 7, 8, 9
- You can specify a step: `range(0, 10, 3)` generates 0, 3, 6, 9
- Negative steps work too: `range(-10, -100, -30)` generates -10, -40, -70

**Common Patterns:**

```python
# Iterate over indices
a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print(i, a[i])

# Better: use enumerate() instead
for i, value in enumerate(a):
    print(i, value)

# Sum a range
sum(range(4))  # Returns 6 (0 + 1 + 2 + 3)
```

### The while Statement
The `while` loop executes as long as a condition is true:

```python
# Print Fibonacci series up to n
a, b = 0, 1
while a < 1000:
    print(a, end=' ')
    a, b = b, a + b
```

## Loop Control Statements

### break Statement
The `break` statement exits the innermost enclosing loop:

```python
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(f"{n} equals {x} * {n//x}")
            break
# Output:
# 4 equals 2 * 2
# 6 equals 2 * 3
# 8 equals 2 * 4
# 9 equals 3 * 3
```

### continue Statement
The `continue` statement skips to the next iteration:

```python
for num in range(2, 10):
    if num % 2 == 0:
        print(f"Found an even number {num}")
        continue
    print(f"Found an odd number {num}")
```

## Common Mistakes

### Infinite Loops
Forgetting to update the loop variable causes infinite loops:

```python
# WRONG - This will loop forever!
x = 0
while x < 10:
    print(x)
    # Missing: x += 1

# CORRECT
x = 0
while x < 10:
    print(x)
    x += 1  # This makes x eventually reach 10
```

### Off-by-One Errors with range()
Remember that `range(n)` goes from 0 to n-1, NOT 0 to n:
- `range(5)` produces: 0, 1, 2, 3, 4
- `range(1, 6)` produces: 1, 2, 3, 4, 5

### Modifying Collection While Iterating
Never modify a list while iterating over it:

```python
# WRONG - unpredictable behavior
for item in my_list:
    if some_condition:
        my_list.remove(item)  # Don't do this!

# CORRECT - iterate over a copy
for item in my_list.copy():
    if some_condition:
        my_list.remove(item)
```

## Source
Content adapted from the official Python Tutorial: https://docs.python.org/3/tutorial/controlflow.html
