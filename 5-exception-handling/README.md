# Exception Handling Example

A small Python example demonstrating how `try`, `except`, and `finally` can be used to handle errors without stopping the program unexpectedly.

## What It Demonstrates

- `try` — code that may raise an exception.
- `except` — handles a specific error.
- `finally` — runs whether an exception occurs or not.

The example takes a number from the user and calculates `10 / number`.

## Why It Matters in Security Tools

Reliable error handling is important in security scripts because unexpected input or runtime errors should be handled predictably. Poor error handling can cause tools to stop unexpectedly or produce confusing results.

This is a **Python fundamentals example**, rather than a standalone security tool.

## Requirements

- Python 3
- No external packages are required.

## Usage

Run:

```bash
python exception_handling.py
```

Example with valid input:

```text
Enter a number: 2
Result: 5.0
Execution completed.
```

Example with invalid input:

```text
Enter a number: abc
Please enter a valid number.
Execution completed.
```

Example with zero:

```text
Enter a number: 0
You cannot divide by zero.
Execution completed.
```

## Skills Demonstrated

- Python exception handling
- `try` / `except` / `finally`
- Input validation
- Handling specific exception types
