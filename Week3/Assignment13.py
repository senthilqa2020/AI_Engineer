import numpy as np

# Generate synthetic dataset: 5 cycles × 50 tests
data = np.random.randint(5, 51, size=(5, 50))
print("Execution Data (5 cycles × 50 tests):\n", data)

print("\n--- 1. Statistical Analysis ---")
# Average execution time per cycle
avg_per_cycle = np.mean(data, axis=1)
print("Average Execution Time per Cycle:", avg_per_cycle)

# Test case with maximum execution time
max_value = np.max(data)
print("Maximum Execution Time in Dataset:", max_value)

# Standard deviation per cycle
std_dev = np.std(data, axis=1)
print("Standard Deviation per Cycle:", std_dev)

print("\n--- 2. Slicing Operations ---")
print("First 10 tests from Cycle 1:", data[0, :10])
print("Last 5 tests from Cycle 5:", data[4, -5:])
print("Every alternate test from Cycle 3:", data[2, ::2])

print("\n--- 3. Arithmetic Operations ---")
print("Cycle1 + Cycle2:", data[0] + data[1])
print("Cycle1 - Cycle2:", data[0] - data[1])
print("Cycle4 * Cycle5:", data[3] * data[4])
print("Cycle4 / Cycle5:", data[3] / data[4])

print("\n--- 4. Power Functions ---")
print("Square of all times:\n", np.power(data, 2))
print("Cube of all times:\n", np.power(data, 3))
print("Square root of all times:\n", np.sqrt(data))
print("Log transform of all times:\n", np.log(data + 1))

print("\n--- 5. Copy Operations ---")
# Shallow copy
shallow = data.view()
shallow[0, :5] = 99  # modify first 5 of cycle 1
print("After modifying shallow copy (original also changes):\n", data[0, :10])

# Deep copy
deep = data.copy()
deep[1, :5] = 77  # modify first 5 of cycle 2
print("After modifying deep copy (original remains unchanged):\n", data[1, :10])

print("\n--- 6. Filtering with Conditions ---")
print("Tests in Cycle 2 > 30 sec:", data[1, data[1] > 30])

# Tests that are >25 in every cycle (across all 5 cycles)
consistent = np.all(data > 25, axis=0)
print("Tests consistently >25 sec across all cycles:", data[:, consistent])

# Replace all <10 with 10 (thresholding)
thresholded = data.copy()
thresholded[thresholded < 10] = 10
print("After thresholding (<10 → 10):\n", thresholded)
