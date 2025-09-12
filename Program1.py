def fizzbuzz(n: int) -> None:
    """Print FizzBuzz from 1 to n inclusive."""
    for i in range(1, n + 1):
        if i % 15 == 0:         # divisible by both 3 and 5
            print("FizzBuzz")
        elif i % 3 == 0:        # divisible by 3 only
            print("Fizz")
        elif i % 5 == 0:        # divisible by 5 only
            print("Buzz")
        else:
            print(str(i))       # neither: print the number


if __name__ == "__main__":
    try:
        n = int(input("Enter a positive integer: "))
        if n <= 0:
            print("Please enter a positive integer greater than 0.")
        else:
            fizzbuzz(n)
    except ValueError:
        print("Invalid input. Please enter an integer number.")

