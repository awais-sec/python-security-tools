def caesar_cipher(text, shift, mode="encrypt"):
    """Encrypt or decrypt a message using a Caesar cipher."""
    result = ""

    if mode == "decrypt":
        shift = -shift

    for char in text:
        if "A" <= char <= "Z":
            base = ord("A")
            result += chr((ord(char) - base + shift) % 26 + base)
        elif "a" <= char <= "z":
            base = ord("a")
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char

    return result


def brute_force(text):
    """Try every possible Caesar cipher shift."""
    print("\nPossible decryptions:")

    for shift in range(1, 26):
        result = caesar_cipher(text, shift, "decrypt")
        print(f"Shift {shift:2}: {result}")


def main():
    print("Caesar Cipher")
    print("1. Encrypt a message")
    print("2. Decrypt a message")
    print("3. Brute-force a message")

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice not in {"1", "2", "3"}:
        print("Invalid choice! Exiting.")
        return

    text = input("Enter the message: ")

    if choice == "3":
        brute_force(text)
        return

    mode = "encrypt" if choice == "1" else "decrypt"

    try:
        shift = int(input("Enter the shift key (1-25): "))
    except ValueError:
        print("Invalid shift key! Must be a number between 1 and 25.")
        return

    if not 1 <= shift <= 25:
        print("Shift key out of range! Must be between 1 and 25.")
        return

    result = caesar_cipher(text, shift, mode)
    print(f"Resulting message: {result}")


if __name__ == "__main__":
    main()
