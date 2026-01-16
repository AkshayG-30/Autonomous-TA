# Lab 3: Working with Python Lists

## Learning Objectives
- Understand list creation and basic operations
- Master common list methods (append, remove, sort, etc.)
- Learn list comprehensions for concise code
- Avoid pitfalls when modifying lists

## Instructions

### Task 1: Student Grade Manager
Create a program that manages a list of student grades.

Requirements:
1. Start with a list of grades: `grades = [85, 92, 78, 90, 88]`
2. Add a new grade (95) to the end of the list
3. Remove the lowest grade from the list
4. Calculate and print the average of the remaining grades
5. Print the grades sorted from highest to lowest

Expected output structure:
```
Original grades: [85, 92, 78, 90, 88]
After adding 95: [85, 92, 78, 90, 88, 95]
After removing lowest: [85, 92, 90, 88, 95]
Average: 90.0
Sorted (high to low): [95, 92, 90, 88, 85]
```

### Task 2: List Comprehensions
Use list comprehensions to create new lists efficiently.

Requirements:
1. Create a list of squares for numbers 1-10: `[1, 4, 9, 16, ...]`
2. Create a list of even numbers from 1-20: `[2, 4, 6, 8, ...]`
3. Create a list of words that are longer than 3 characters from: `["hi", "hello", "cat", "world", "to"]`

### Task 3: List Operations
Given two lists, perform set-like operations.

Requirements:
1. Given `list_a = [1, 2, 3, 4, 5]` and `list_b = [4, 5, 6, 7, 8]`
2. Find elements that appear in both lists
3. Find elements that are in list_a but not in list_b
4. Combine both lists without duplicates

## Common Mistakes

### Modifying a List While Iterating
Never remove items from a list while looping over it:

```python
# WRONG - this skips elements!
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)  # [1, 3, 5] but might miss some!

# CORRECT - iterate over a copy
numbers = [1, 2, 3, 4, 5]
for n in numbers.copy():
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)  # [1, 3, 5]

# BETTER - use list comprehension
numbers = [1, 2, 3, 4, 5]
numbers = [n for n in numbers if n % 2 != 0]
```

### Off-by-One Index Errors
Remember that list indices start at 0:

```python
fruits = ["apple", "banana", "cherry"]

# WRONG - index 3 doesn't exist!
# print(fruits[3])  # IndexError

# CORRECT - valid indices are 0, 1, 2
print(fruits[0])  # "apple"
print(fruits[2])  # "cherry"
print(fruits[-1]) # "cherry" (last element)
```

### Confusing sort() and sorted()
`sort()` modifies in place, `sorted()` returns a new list:

```python
numbers = [3, 1, 4, 1, 5]

# sort() changes the original list, returns None
result = numbers.sort()
print(result)   # None
print(numbers)  # [1, 1, 3, 4, 5]

# sorted() returns a new list, original unchanged
numbers = [3, 1, 4, 1, 5]
result = sorted(numbers)
print(result)   # [1, 1, 3, 4, 5]
print(numbers)  # [3, 1, 4, 1, 5] (unchanged)
```

### Creating Shallow Copies
Assignment creates a reference, not a copy:

```python
# WRONG - both variables point to same list
original = [1, 2, 3]
copy = original
copy.append(4)
print(original)  # [1, 2, 3, 4] - original changed too!

# CORRECT - create an actual copy
original = [1, 2, 3]
copy = original.copy()  # or list(original) or original[:]
copy.append(4)
print(original)  # [1, 2, 3] - original unchanged
```

## Grading Criteria
- Correct list operations: 40%
- List comprehensions used appropriately: 25%
- Handles edge cases (empty lists, etc.): 15%
- Code style and readability: 20%

## Source
Based on Python Tutorial: https://docs.python.org/3/tutorial/datastructures.html
