# Program 8: List Slicing and Indexing

# Given list of first ten prime numbers
prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

# a) Extract the middle five primes
middle_five = prime_numbers[2:7]

# b) Get every second prime (starting from beginning)
every_second = prime_numbers[::2]

# c) Use negative indexing to get last three primes
last_three = prime_numbers[-3:]

# d) Reverse the list
reversed_list = prime_numbers[::-1]

# e) Descending order sort
descending_sorted = sorted(prime_numbers, reverse=True)

# Print results
print("Original List       :", prime_numbers)
print("Middle Five Primes  :", middle_five)
print("Every Second Prime  :", every_second)
print("Last Three Primes   :", last_three)
print("Reversed List       :", reversed_list)
print("Descending Order    :", descending_sorted)
