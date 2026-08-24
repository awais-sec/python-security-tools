# Dictionary Attack Demo

A simple Python lab that demonstrates how a password dictionary can be used to test a known target password against a list of candidate passwords.

## What It Does

The tool:

- Loads passwords from a text file.
- Tests each candidate against the target password.
- Stops when a matching password is found.
- Reports when the password is not present in the supplied list.

## Why It Is a Security Tool

Dictionary attacks demonstrate how attackers can test commonly used or previously exposed passwords against an authentication target. The lab helps explain why strong, unique passwords and protections such as rate limiting and account lockout are important.

> This implementation is a local educational demonstration. It does not connect to or attack a real authentication service.

## Requirements

- Python 3
- No external packages are required.
- A text file containing candidate passwords, one per line.

## Usage

Run the script:

```bash
python dictionary_attack.py
```

The program asks for the target password and the path to the password dictionary:

```text
Enter the target password: password123
Enter the path to the password dictionary file: passwords.txt
```

The tool then tests each entry in the file until it finds a match.

## Example Dictionary

```text
admin
password
letmein
password123
qwerty
```

## How It Works

The program reads the dictionary file into a list and compares each candidate password with the supplied target password.

This is intentionally a simplified demonstration of the **dictionary-attack concept** rather than a real authentication attack tool.

## Limitations

- The target password is supplied directly to the program.
- It does not interact with a login service.
- It does not perform online authentication attempts.
- It does not use password hashing or cracking algorithms.
- It only tests passwords contained in the supplied dictionary.

## Skills Demonstrated

- Python file handling
- Lists and iteration
- Password-guessing concepts
- Basic error handling
- Security awareness around weak passwords
