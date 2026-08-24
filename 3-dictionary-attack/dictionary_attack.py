"""
DISCLAIMER: This tool is for EDUCATIONAL PURPOSES ONLY.
Use only on systems you own or have explicit permission to test.
Unauthorized access is illegal and unethical.
"""


def load_passwords(file_path):
    """Load passwords from a text file."""
    try:
        with open(file_path, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print("Password file not found.")
        return []


def brute_force(target_password, password_list):
    """Try each password in the list until a match is found."""
    for password in password_list:
        print(f"Trying password: {password}")

        if password == target_password:
            print(f"Password found: {password}")
            return True

    print("Password not found in the list.")
    return False


def main():
    target_password = input("Enter the target password: ")
    password_file = input("Enter the path to the password dictionary file: ").strip()

    password_list = load_passwords(password_file)

    if password_list:
        brute_force(target_password, password_list)


if __name__ == "__main__":
    main()
