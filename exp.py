# write a function to print multiplication tabels

def print_multiplication_table(number):
    """Prints the multiplication table for a given number."""
    print(f"Multiplication table for {number}:")
    for i in range(1, 11):
        print(f"{number} x {i} = {number * i}")
    print("\n")  # Add a newline for better readability

print_multiplication_table(2)