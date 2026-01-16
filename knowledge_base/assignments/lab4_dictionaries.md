# Lab 4: Working with Python Dictionaries

## Learning Objectives
- Understand dictionary creation and key-value pairs
- Master dictionary methods (get, keys, values, items)
- Learn dictionary comprehensions
- Handle common dictionary errors gracefully

## Instructions

### Task 1: Simple Phonebook
Create a phonebook application using a dictionary.

Requirements:
1. Create a dictionary with at least 3 contacts: `{"Alice": "555-1234", ...}`
2. Add a new contact to the phonebook
3. Look up a phone number by name
4. Delete a contact from the phonebook
5. Print all contacts in a formatted way

Example output:
```
Looking up Alice: 555-1234
Looking up Unknown: Contact not found

All contacts:
  Alice: 555-1234
  Bob: 555-5678
  Charlie: 555-9012
```

### Task 2: Word Counter
Count the frequency of each word in a sentence.

Requirements:
1. Take input sentence: "the quick brown fox jumps over the lazy fox"
2. Create a dictionary with each word as key and count as value
3. Print the word counts
4. Find and print the most common word

Expected output:
```
Word counts: {'the': 2, 'quick': 1, 'brown': 1, 'fox': 2, ...}
Most common word: 'the' (appears 2 times)
```

### Task 3: Student Records
Create a dictionary of student records where each student has multiple attributes.

Requirements:
1. Create records for 3 students with name, age, and grade
2. Add a new attribute (email) to an existing student
3. Print a formatted report of all students

Structure:
```python
students = {
    "S001": {"name": "Alice", "age": 20, "grade": "A"},
    ...
}
```

## Common Mistakes

### KeyError When Accessing Missing Keys
Don't access dictionary keys directly without checking:

```python
phonebook = {"Alice": "555-1234"}

# WRONG - raises KeyError if key doesn't exist
# number = phonebook["Bob"]  # KeyError: 'Bob'

# CORRECT - use get() with a default value
number = phonebook.get("Bob", "Not found")
print(number)  # "Not found"

# CORRECT - check if key exists first
if "Bob" in phonebook:
    print(phonebook["Bob"])
else:
    print("Contact not found")
```

### Using Mutable Objects as Keys
Dictionary keys must be immutable (hashable):

```python
# WRONG - lists are mutable, can't be keys
# my_dict = {[1, 2]: "value"}  # TypeError: unhashable type: 'list'

# CORRECT - use tuples instead (they're immutable)
my_dict = {(1, 2): "value"}
print(my_dict[(1, 2)])  # "value"

# Valid key types: strings, numbers, tuples (of immutables)
valid_dict = {
    "name": "Alice",
    42: "a number key",
    (1, 2): "a tuple key"
}
```

### Modifying Dictionary While Iterating
Don't change dictionary size during iteration:

```python
scores = {"Alice": 85, "Bob": 72, "Charlie": 90}

# WRONG - can't change dict size while iterating
# for name, score in scores.items():
#     if score < 80:
#         del scores[name]  # RuntimeError!

# CORRECT - iterate over a copy of keys
for name in list(scores.keys()):
    if scores[name] < 80:
        del scores[name]

# BETTER - use dictionary comprehension
scores = {name: score for name, score in scores.items() if score >= 80}
```

### Overwriting Keys Accidentally
Each key can only have one value:

```python
phonebook = {"Alice": "555-1234"}

# This REPLACES the old value, doesn't add to it
phonebook["Alice"] = "555-9999"
print(phonebook)  # {"Alice": "555-9999"}

# If you need multiple values, use a list
phonebook = {"Alice": ["555-1234", "555-9999"]}
```

## Useful Dictionary Patterns

### Safe Key Access with setdefault()
```python
# Add key only if it doesn't exist
phonebook.setdefault("Dave", "Unknown")
```

### Merging Dictionaries
```python
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

# Python 3.9+
merged = dict1 | dict2

# Older Python
merged = {**dict1, **dict2}
```

## Grading Criteria
- Correct dictionary operations: 35%
- Handles missing keys gracefully: 25%
- Clean iteration over dictionary items: 20%
- Code style and formatting: 20%

## Source
Based on Python Tutorial: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
