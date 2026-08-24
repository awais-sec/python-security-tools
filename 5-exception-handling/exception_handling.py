try:
    number = int(input("Enter a number: "))
    print("Result:", 10 / number)
except ValueError:
    print("Please enter a valid number.")
except ZeroDivisionError:
    print("You cannot divide by zero.")
finally:
    print("Execution completed.")
