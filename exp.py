# create a function for print the multiplication table
def print_multiplication_table(n):
    """Print the multiplication table of n."""
    for i in range(1, 11):
        print(f"{n} x {i} = {n * i}")

print_multiplication_table(5)