# Program: Managing Student Records (Assignment 7)

class Student:
    def __init__(self, name: str, grade: str, department: str):
        self.name = name
        self.grade = grade
        self.department = department

    def print_info(self) -> None:
        """Print all details of the student in a readable format."""
        print(f"Name       : {self.name}")
        print(f"Grade      : {self.grade}")
        print(f"Department : {self.department}")
        print("-" * 30)

    def update_grade(self, new_grade: str) -> None:
        """Update the student's grade."""
        self.grade = new_grade


def print_all_students(students: list) -> None:
    """Helper to display multiple student records."""
    print("\n=== Student Records ===")
    for s in students:
        s.print_info()


if __name__ == "__main__":
    # Create at least three Student objects with different details
    student1 = Student("Aarav Kumar", "A", "Computer Science")
    student2 = Student("Diya Sharma", "B", "Electronics")
    student3 = Student("Vikram Rao", "C", "Mechanical")

    # Store multiple students in a list for easy management
    students = [student1, student2, student3]

    # Print each student's information
    print_all_students(students)

    # Update the grade of one student and print the updated details
    print(">>> Updating Diya's grade from B to A- ...\n")
    student2.update_grade("A-")

    # Show updated records
    print_all_students(students)

    # --- Optional: demonstrate adding a new record dynamically ---
    # new_student = Student("Neha Gupta", "B+", "Information Technology")
    # students.append(new_student)
    # print_all_students(students)
