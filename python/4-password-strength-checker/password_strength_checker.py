import re


def validate_password_strength(password):
    """Check a password and return feedback about its strength."""
    if not password or password.strip() == "":
        return {
            "is_strong": False,
            "feedback": ["Password cannot be empty."]
        }

    issues = []

    if len(password) < 8:
        issues.append("at least 8 characters long")

    if not re.search(r"[A-Z]", password):
        issues.append("at least one uppercase letter")

    if not re.search(r"[a-z]", password):
        issues.append("at least one lowercase letter")

    if not re.search(r"\d", password):
        issues.append("at least one digit")

    if not re.search(r"[!@#$%^&*(),.?\"{}|<>_~\-]", password):
        issues.append("at least one special character")

    if issues:
        return {
            "is_strong": False,
            "feedback": [f"Password must contain {issue}" for issue in issues]
        }

    return {
        "is_strong": True,
        "feedback": ["Password meets all strength requirements."]
    }


def main():
    print("=" * 50)
    print("PASSWORD STRENGTH CHECKER")
    print("=" * 50)
    print("\nA strong password should have:")
    print("- At least 8 characters")
    print("- Uppercase and lowercase letters")
    print("- At least one number")
    print("- At least one special character")

    password = input("\nEnter a password to check: ")
    result = validate_password_strength(password)

    print("\n" + "=" * 50)

    if result["is_strong"]:
        print("Password is strong!")
    else:
        print("Password is weak. Please fix the following:")
        for issue in result["feedback"]:
            print(f"- {issue}")

    print("=" * 50)


if __name__ == "__main__":
    main()
