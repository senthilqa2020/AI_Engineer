
# Calculate total, average, highest, and lowest sales.

# 1) Store the sales data in a list
sales = [1200, 3400, 560, 4500, 2100]

# 2) Use built-in functions to compute summary stats
total_sales = sum(sales)
average_sales = total_sales / len(sales)
highest_sale = max(sales)
lowest_sale = min(sales)

# 3) Print results
print("Total Sales:", total_sales)
print("Average Sales:", average_sales)
print("Highest Sale:", highest_sale)
print("Lowest Sale:", lowest_sale)
