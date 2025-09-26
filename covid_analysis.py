import pandas as pd
import numpy as np

# ---------------------------
# Base Class for Data Loading
# ---------------------------
class CovidDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)

    def get_data(self):
        return self.df


# -----------------------------------------
# Derived Class for Covid Data Analysis
# -----------------------------------------
class CovidDataAnalysis(CovidDataLoader):
    def __init__(self, file_path):
        super().__init__(file_path)

    # 1. Summarize Case Counts by Region
    def summarize_by_region(self):
        summary = self.df.groupby("WHO Region")[["Confirmed", "Deaths", "Recovered"]].sum()
        print("\n--- Total Confirmed, Deaths, and Recovered by Region ---")
        print(summary)
        return summary

    # 2. Filter Low Case Records (<10 confirmed)
    def filter_low_cases(self):
        filtered = self.df[self.df["Confirmed"] >= 10]
        print("\n--- Filtered Data (Confirmed >= 10) ---")
        print(filtered.head())
        return filtered

    # 3. Region with Highest Confirmed Cases
    def highest_confirmed_region(self):
        region = self.df.groupby("WHO Region")["Confirmed"].sum().idxmax()
        print("\nRegion with Highest Confirmed Cases:", region)
        return region

    # 4. Sort Data by Confirmed Cases and Save
    def sort_by_confirmed(self, output_file="sorted_covid_cases.csv"):
        sorted_df = self.df.sort_values(by="Confirmed", ascending=False)
        sorted_df.to_csv(output_file, index=False)
        print(f"\nSorted dataset saved to {output_file}")
        return sorted_df

    # 5. Top 5 Countries by Case Count
    def top5_countries(self):
        top5 = self.df.groupby("Country/Region")["Confirmed"].sum().nlargest(5)
        print("\n--- Top 5 Countries by Confirmed Cases ---")
        print(top5)
        return top5

    # 6. Region with Lowest Death Count
    def lowest_death_region(self):
        region = self.df.groupby("WHO Region")["Deaths"].sum().idxmin()
        print("\nRegion with Lowest Death Count:", region)
        return region

    # 7. India’s Case Summary (as of April 29, 2020)
    def india_summary(self):
        india = self.df[self.df["Country/Region"] == "India"]
        print("\n--- India’s Case Summary ---")
        print(india)
        return india

    # 8. Calculate Mortality Rate by Region
    def mortality_rate(self):
        rates = self.df.groupby("WHO Region").apply(
            lambda x: x["Deaths"].sum() / x["Confirmed"].sum() if x["Confirmed"].sum() > 0 else 0
        )
        print("\n--- Mortality Rate by Region (Deaths/Confirmed) ---")
        print(rates)
        return rates

    # 9. Compare Recovery Rates Across Regions
    def recovery_rate(self):
        rates = self.df.groupby("WHO Region").apply(
            lambda x: x["Recovered"].sum() / x["Confirmed"].sum() if x["Confirmed"].sum() > 0 else 0
        )
        print("\n--- Recovery Rate by Region (Recovered/Confirmed) ---")
        print(rates)
        return rates

    # 10. Detect Outliers in Case Counts (mean ± 2*std)
    def detect_outliers(self):
        confirmed = self.df["Confirmed"]
        mean, std = confirmed.mean(), confirmed.std()
        lower, upper = mean - 2 * std, mean + 2 * std
        outliers = self.df[(confirmed < lower) | (confirmed > upper)]
        print("\n--- Outliers in Confirmed Cases ---")
        print(outliers)
        return outliers

    # 11. Group Data by Country and Region
    def group_country_region(self):
        grouped = self.df.groupby(["Country/Region", "WHO Region"])[["Confirmed", "Deaths", "Recovered"]].sum()
        print("\n--- Grouped Data by Country and Region ---")
        print(grouped.head())
        return grouped

    # 12. Identify Regions with Zero Recovered Cases
    def zero_recovered_regions(self):
        zero_regions = self.df.groupby("WHO Region")["Recovered"].sum()
        zero_regions = zero_regions[zero_regions == 0]
        print("\nRegions with Zero Recovered Cases:")
        print(zero_regions)
        return zero_regions


# ---------------------------
# Main Execution
# ---------------------------
if __name__ == "__main__":
    file_path = "country_wise_latest.csv"   # Ensure dataset is in same folder
    analysis = CovidDataAnalysis(file_path)

    analysis.summarize_by_region()
    analysis.filter_low_cases()
    analysis.highest_confirmed_region()
    analysis.sort_by_confirmed()
    analysis.top5_countries()
    analysis.lowest_death_region()
    analysis.india_summary()
    analysis.mortality_rate()
    analysis.recovery_rate()
    analysis.detect_outliers()
    analysis.group_country_region()
    analysis.zero_recovered_regions()
