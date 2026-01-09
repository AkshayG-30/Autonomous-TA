# Lab 1: Introduction to Python Loops

## Learning Objectives
- Understand the difference between `for` and `while` loops
- Learn how to properly initialize and update loop variables
- Avoid common pitfalls like infinite loops

## Instructions

### Task 1: Sum of Numbers
Write a program that calculates the sum of numbers from 1 to N, where N is provided by the user.

Requirements:
1. Use a `for` loop with `range()`
2. Print the final sum
3. Handle the case where N is negative (print an error message)

### Task 2: Counting Down
Write a program that counts down from a given number to 1, printing each number.

Requirements:
1. Use a `while` loop
2. Make sure to update your counter variable inside the loop to avoid infinite loops!
3. Print "Liftoff!" after reaching 1

## Common Mistakes

### Infinite Loops
The most common mistake is forgetting to update the loop variable inside a while loop:

```python
# WRONG - This will loop forever!
x = 0
while x < 10:
    print(x)
    # Missing: x = x + 1 or x += 1

# CORRECT
x = 0
while x < 10:
    print(x)
    x += 1  # This makes x eventually reach 10
```

### Off-by-One Errors
Remember that `range(n)` goes from 0 to n-1, not 0 to n:
- `range(5)` produces: 0, 1, 2, 3, 4
- `range(1, 6)` produces: 1, 2, 3, 4, 5

## Grading Criteria
- Correct output: 40%
- Code style (proper indentation, meaningful variable names): 30%
- Handles edge cases: 30%
