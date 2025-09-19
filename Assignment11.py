import numpy as ab

# Base class
class TestReport:
    def __init__(self, execution_times):
        # Store execution times as a NumPy array
        self.execution_times = ab.array(execution_times)

    def average_time(self):
        """Return the mean execution time"""
        return ab.mean(self.execution_times)

    def max_time(self):
        """Return the maximum execution time"""
        return ab.max(self.execution_times)


# Subclass
class RegressionReport(TestReport):
    def __init__(self, execution_times):
        # Call parent constructor
        super().__init__(execution_times)

    def slow_tests(self, threshold):
        """Return tests taking more than threshold seconds"""
        return self.execution_times[self.execution_times > threshold]


# Main section
if __name__ == "__main__":
    # Create a NumPy array with 10 execution times (in seconds)
    times = ab.array([12, 8, 15, 6, 20, 14, 9, 11, 18, 7])

    # Create RegressionReport object
    report = RegressionReport(times)

    # Display results
    print("Average Execution Time:", report.average_time())
    print("Maximum Execution Time:", report.max_time())
    print("Slow Tests (>10s):", report.slow_tests(10))