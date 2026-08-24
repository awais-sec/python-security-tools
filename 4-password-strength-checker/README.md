# Password Strength Checker

A simple Python tool that checks whether a password meets a set of basic strength requirements and explains what is missing when it does not.

## What It Checks

The checker looks for:

- At least 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

## Why It Is a Security Tool

Weak passwords are an important security risk. This tool demonstrates some basic password-strength requirements that can help users avoid simple, easily guessable passwords.

It is a **rule-based checker**, not a complete password-security assessment.

## Requirements

- Python 3
- No external packages are required.

## Usage

Run the script:

```bash
python password_strength_checker.py
```

Enter a password when prompted:

```text
Enter a password to check: Password123!

==================================================
Password is strong!
==================================================
```

For a password that does not meet the requirements, the tool lists the missing requirements.

## How It Works

The program uses Python's `re` module to check the password for different character types. It collects any missing requirements and returns them as feedback.

The password itself is only used during the local check and is not sent to a network service or stored by the program.

## Limitations

This tool should not be treated as a definitive measure of password security. In particular, it does not:

- Check passwords against known breached-password lists.
- Estimate password entropy.
- Detect common words or predictable patterns.
- Measure resistance to modern password-cracking techniques.
- Account for password length beyond the minimum requirement.

A long passphrase can be stronger than a short password that simply satisfies several character rules.

## Skills Demonstrated

- Python regular expressions
- Input validation
- Conditional logic
- Function design
- Basic password-security concepts
