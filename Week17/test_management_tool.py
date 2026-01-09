import csv

# -----------------------------
# Step 1: TestCase Class
# -----------------------------
class TestCase:
    def __init__(self, test_id, test_name, module, status="Not Executed"):
        self.test_id = test_id
        self.test_name = test_name
        self.module = module
        self.status = status

    def execute_test(self, result):
        self.status = result

    def display_test_case(self):
        print(f"ID: {self.test_id}, Name: {self.test_name}, "
              f"Module: {self.module}, Status: {self.status}")

    def to_csv_row(self):
        return [self.test_id, self.test_name, self.module, self.status, "NA"]


# -----------------------------
# Step 2: AutomatedTestCase Class
# -----------------------------
class AutomatedTestCase(TestCase):
    def __init__(self, test_id, test_name, module, automation_tool, status="Not Executed"):
        super().__init__(test_id, test_name, module, status)
        self.automation_tool = automation_tool

    def display_test_case(self):
        print(f"ID: {self.test_id}, Name: {self.test_name}, "
              f"Module: {self.module}, Status: {self.status}, "
              f"Tool: {self.automation_tool}")

    def to_csv_row(self):
        return [self.test_id, self.test_name, self.module,
                self.status, self.automation_tool]


# -----------------------------
# Step 3: TestSuite Class
# -----------------------------
class TestSuite:
    def __init__(self, suite_name):
        self.suite_name = suite_name
        self.test_cases = []

    def add_test(self, test_case):
        self.test_cases.append(test_case)

    def run_all_tests(self):
        print(f"\nExecuting Test Suite: {self.suite_name}\n")
        for test in self.test_cases:
            test.display_test_case()
            result = input("Enter result (Pass/Fail): ")
            test.execute_test(result)

    def save_results_to_csv(self, file_name):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Test ID", "Test Name", "Module", "Status", "Automation Tool"]
            )
            for test in self.test_cases:
                writer.writerow(test.to_csv_row())

    def summary_report(self):
        total = len(self.test_cases)
        passed = sum(1 for t in self.test_cases if t.status == "Pass")
        failed = sum(1 for t in self.test_cases if t.status == "Fail")
        not_executed = sum(1 for t in self.test_cases if t.status == "Not Executed")

        print("\n--- Test Execution Summary ---")
        print(f"Total Tests       : {total}")
        print(f"Passed Tests      : {passed}")
        print(f"Failed Tests      : {failed}")
        print(f"Not Executed Tests: {not_executed}")


# -----------------------------
# Step 5: Main Program
# -----------------------------
if __name__ == "__main__":
    # Manual Test Cases
    tc1 = TestCase("TC001", "Login Validation", "Authentication")
    tc2 = TestCase("TC002", "Logout Validation", "Authentication")

    # Automated Test Cases
    atc1 = AutomatedTestCase("TC003", "Add to Cart", "Cart", "Selenium")
    atc2 = AutomatedTestCase("TC004", "Payment Flow", "Checkout", "Playwright")

    # Create Test Suite
    suite = TestSuite("Regression Suite")

    # Add Tests
    suite.add_test(tc1)
    suite.add_test(tc2)
    suite.add_test(atc1)
    suite.add_test(atc2)

    # Execute Tests
    suite.run_all_tests()

    # Save Results
    suite.save_results_to_csv("test_results.csv")

    # Print Summary
    suite.summary_report()
