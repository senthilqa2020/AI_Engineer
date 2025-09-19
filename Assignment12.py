import numpy as np

# Base role classes
class ManualTester:
    def analyze(self, data):
        # Show the first 5 execution times
        print("ManualTester - First 5 Execution Times:", data[:5])


class AutomationTester:
    def analyze(self, data):
        # Show the fastest test execution time
        print("AutomationTester - Fastest Test Case:", np.min(data))


class PerformanceTester:
    def analyze(self, data):
        # Show the 95th percentile execution time
        print("PerformanceTester - 95th Percentile Execution Time:", np.percentile(data, 95))


# Polymorphism function
def show_analysis(tester, data):
    tester.analyze(data)


# Main execution
if __name__ == "__main__":
    # Create a NumPy array with at least 12 execution times
    execution_times = np.array([12, 8, 15, 6, 20, 14, 9, 11, 18, 7, 22, 10])

    # Create tester role objects
    manual = ManualTester()
    automation = AutomationTester()
    performance = PerformanceTester()

    # Demonstrate polymorphism
    show_analysis(manual, execution_times)
    show_analysis(automation, execution_times)
    show_analysis(performance, execution_times)
