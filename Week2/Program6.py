# Program: Book Class Implementation
# Matches the assignment: title, author, publication_year, and get_age()

import datetime

class Book:
    def __init__(self, title: str, author: str, publication_year: int):
        self.title = title
        self.author = author
        self.publication_year = publication_year

    def get_age(self) -> int:
        """Return the age of the book in years (current year - publication_year)."""
        current_year = datetime.datetime.now().year
        return current_year - self.publication_year


if __name__ == "__main__":
    # Example usage (as shown in the assignment)
    book1 = Book("Python Basics", "John Doe", 2015)
    print("Book Age:", book1.get_age(), "years")

    # --- Optional: interactive input (useful for quick testing in the terminal) ---
    try:
        print("\nEnter your own book details:")
        title = input("Title: ").strip()
        author = input("Author: ").strip()
        pub_year = int(input("Publication year (e.g., 2015): ").strip())

        user_book = Book(title, author, pub_year)
        print("Book Age:", user_book.get_age(), "years")
    except ValueError:
        print("Please enter a valid number for the publication year.")
