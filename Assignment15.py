Assignment15.py
# Modeling an IT Organization using Inheritance

# Base class
class Employee:
    def __init__(self, name, emp_id, department):
        self.name = name
        self.emp_id = emp_id
        self.department = department

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Employee ID: {self.emp_id}")
        print(f"Department: {self.department}")


# Subclass Manager
class Manager(Employee):
    def __init__(self, name, emp_id, department, team_size):
        # Call parent constructor
        super().__init__(name, emp_id, department)
        self.team_size = team_size

    def display_info(self):
        # Extend parent method
        super().display_info()
        print(f"Team Size: {self.team_size}")


# Subclass Developer
class Developer(Employee):
    def __init__(self, name, emp_id, department, programming_language):
        # Call parent constructor
        super().__init__(name, emp_id, department)
        self.programming_language = programming_language

    def display_info(self):
        # Extend parent method
        super().display_info()
        print(f"Programming Language: {self.programming_language}")


# Main section
if __name__ == "__main__":
    # Create Manager and Developer objects
    manager = Manager("Alice Johnson", "M001", "QA", 10)
    developer = Developer("Bob Smith", "D101", "IT", "Python")

    # Display their details
    print("Manager Information:")
    manager.display_info()
    print("\nDeveloper Information:")
    developer.display_info()
