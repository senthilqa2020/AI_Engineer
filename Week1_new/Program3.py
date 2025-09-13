
# Print a numbered list of employee names

def print_employee_list():
    # 1) Maintain a list of 5 employee names (hardcoded)
    employees = ["Alice", "Bob", "Charlie", "David", "Eve"]

    # 2) Print each name numbered 1..N
    for i, name in enumerate(employees, start=1):
        print(f"{i}. {name}")

# Main entry point
if __name__ == "__main__":
    print_employee_list()

