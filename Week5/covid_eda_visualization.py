#!/usr/bin/env python3
# covid_eda_visualization.py
# Usage:
#   python covid_eda_visualization.py --csv country_wise_latest.csv --out charts
#
# Notes:
# - Creates an output folder (default: charts) and saves all images there.
# - Uses only matplotlib (no seaborn) as requested in many coursework rules.

import argparse
import os
from pathlib import Path
import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class CovidAnalysis:
    """
    Loads and prepares COVID-19 data for analysis.

    Expected columns (common in country_wise_latest.csv from Kaggle):
      Country/Region, Confirmed, Deaths, Recovered, Active, WHO Region
    """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = self._load()

    def _load(self) -> pd.DataFrame:
        if not Path(self.csv_path).exists():
            raise FileNotFoundError(
                f"CSV not found: {self.csv_path}\n"
                "Tip: put 'country_wise_latest.csv' next to this script, or pass --csv <path>."
            )
        df = pd.read_csv(self.csv_path)

        # Normalize expected column names if there are small variations
        rename_map = {
            "Country_Region": "Country/Region",
            "Country": "Country/Region",
            "WHO_Region": "WHO Region",
            "Region": "WHO Region",
        }
        df = df.rename(columns=rename_map)

        # Ensure essential columns exist
        required = ["Country/Region", "Confirmed", "Deaths", "Recovered"]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Expected column '{col}' not found in CSV.")

        # If WHO Region missing, create a placeholder
        if "WHO Region" not in df.columns:
            df["WHO Region"] = "Unknown"

        # Fill numeric NaNs with zeros
        for col in ["Confirmed", "Deaths", "Recovered"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        # Derive Active if missing
        if "Active" not in df.columns:
            df["Active"] = (df["Confirmed"] - df["Deaths"] - df["Recovered"]).clip(lower=0)

        return df

    # Helper data slices used by visualization
    def top_n_by_confirmed(self, n=10) -> pd.DataFrame:
        return self.df.nlargest(n, "Confirmed")[["Country/Region", "Confirmed", "Deaths", "Recovered", "Active"]]

    def region_group(self) -> pd.DataFrame:
        return (
            self.df.groupby("WHO Region", dropna=False)[["Confirmed", "Deaths", "Recovered", "Active"]]
            .sum()
            .sort_values("Confirmed", ascending=False)
        )

    def country_slice(self, countries: list[str]) -> pd.DataFrame:
        return (
            self.df[self.df["Country/Region"].isin(countries)]
            .set_index("Country/Region")[["Confirmed", "Deaths", "Recovered"]]
            .sort_values("Confirmed", ascending=False)
        )


class CovidVisualization(CovidAnalysis):
    """Adds plotting/EDA methods on top of CovidAnalysis."""

    def __init__(self, csv_path: str, out_dir: str = "charts"):
        super().__init__(csv_path)
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        # Matplotlib warnings (fonts, etc.) can be noisy in some setups—silence non-critical ones
        warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

    # Utility: save and close
    def _save(self, name: str):
        out_path = self.out_dir / f"{name}.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=160, bbox_inches="tight")
        plt.close()
        print(f"Saved: {out_path}")

    # 1) Bar Chart of Top 10 Countries by Confirmed Cases
    def bar_top10_confirmed(self):
        data = self.top_n_by_confirmed(10)
        plt.figure(figsize=(10, 5))
        plt.bar(data["Country/Region"], data["Confirmed"])
        plt.title("Top 10 Countries by Confirmed Cases")
        plt.xlabel("Country")
        plt.ylabel("Confirmed Cases")
        plt.xticks(rotation=45, ha="right")
        self._save("1_bar_top10_confirmed")

    # 2) Pie Chart of Global Death Distribution by Region
    def pie_deaths_by_region(self):
        grp = self.region_group()
        values = grp["Deaths"]
        labels = grp.index.astype(str)
        plt.figure(figsize=(7, 7))
        # Avoid too many labels if there are many "Unknown"—show up to 8 largest
        if len(values) > 8:
            top_vals = values.nlargest(7)
            others = values.drop(top_vals.index).sum()
            values = pd.concat([top_vals, pd.Series({"Others": others})])
            labels = values.index
        plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title("Global Death Distribution by WHO Region")
        self._save("2_pie_deaths_by_region")

    # 3) Line Chart comparing Confirmed and Deaths for Top 5 Countries
    def line_confirmed_vs_deaths_top5(self):
        top5 = self.top_n_by_confirmed(5).set_index("Country/Region")
        plt.figure(figsize=(9, 5))
        plt.plot(top5.index, top5["Confirmed"], marker="o", label="Confirmed")
        plt.plot(top5.index, top5["Deaths"], marker="o", label="Deaths")
        plt.title("Confirmed vs Deaths – Top 5 Countries")
        plt.xlabel("Country")
        plt.ylabel("Count")
        plt.legend()
        plt.xticks(rotation=20, ha="right")
        self._save("3_line_confirmed_vs_deaths_top5")

    # 4) Scatter Plot of Confirmed vs Recovered Cases
    def scatter_confirmed_vs_recovered(self):
        plt.figure(figsize=(7, 5))
        plt.scatter(self.df["Confirmed"], self.df["Recovered"], alpha=0.6)
        plt.title("Confirmed vs Recovered (All Countries)")
        plt.xlabel("Confirmed")
        plt.ylabel("Recovered")
        self._save("4_scatter_confirmed_vs_recovered")

    # 5) Histogram of Death Counts across all Regions (country-level distribution)
    def hist_deaths_all_regions(self):
        plt.figure(figsize=(8, 5))
        plt.hist(self.df["Deaths"], bins=30)
        plt.title("Histogram of Death Counts (Country Level)")
        plt.xlabel("Deaths")
        plt.ylabel("Frequency")
        self._save("5_hist_deaths_all_regions")

    # 6) Stacked Bar Chart of Confirmed, Deaths, Recovered for 5 Selected Countries
    def stacked_bar_selected_countries(self, countries=None):
        if countries is None:
            countries = ["India", "United States", "Brazil", "Russia", "United Kingdom"]
        data = self.country_slice(countries)
        x = np.arange(len(data.index))
        width = 0.6

        plt.figure(figsize=(10, 6))
        plt.bar(x, data["Confirmed"], width, label="Confirmed")
        plt.bar(x, data["Deaths"], width, bottom=data["Confirmed"], label="Deaths")
        bottom2 = data["Confirmed"] + data["Deaths"]
        plt.bar(x, data["Recovered"], width, bottom=bottom2, label="Recovered")
        plt.xticks(x, data.index, rotation=20, ha="right")
        plt.title("Stacked Cases for Selected Countries")
        plt.xlabel("Country")
        plt.ylabel("Count")
        plt.legend()
        self._save("6_stacked_confirmed_deaths_recovered")

    # 7) Box Plot of Confirmed Cases across Regions
    def boxplot_confirmed_by_region(self):
        grp = self.df[["WHO Region", "Confirmed"]].copy()
        groups = [g["Confirmed"].values for _, g in grp.groupby("WHO Region")]
        labels = [str(k) for k, _ in grp.groupby("WHO Region")]
        plt.figure(figsize=(10, 5))
        plt.boxplot(groups, labels=labels, showfliers=False)
        plt.title("Box Plot: Confirmed Cases by WHO Region")
        plt.xlabel("WHO Region")
        plt.ylabel("Confirmed")
        plt.xticks(rotation=20, ha="right")
        self._save("7_boxplot_confirmed_by_region")

    # 8) Trend Line: Plot Confirmed for India vs another country (side-by-side bars act as 'trend' snapshot)
    # If your dataset had time series, we'd plot over time; this snapshot compares totals.
    def trendline_india_vs(self, other_country="United States"):
        countries = ["India", other_country]
        data = self.country_slice(countries)
        data = data.reindex(countries)  # keep order

        plt.figure(figsize=(7, 5))
        plt.bar(data.index, data["Confirmed"])
        plt.title(f"Confirmed Cases: India vs {other_country}")
        plt.xlabel("Country")
        plt.ylabel("Confirmed")
        self._save(f"8_trend_india_vs_{other_country.replace(' ', '_')}")


def main():
    parser = argparse.ArgumentParser(description="COVID-19 EDA & Visualization (Matplotlib + Pandas).")
    parser.add_argument("--csv", default="country_wise_latest.csv", help="Path to country_wise_latest.csv")
    parser.add_argument("--out", default="charts", help="Output folder to save charts")
    parser.add_argument("--other", default="United States", help="Other country for the India comparison")
    args = parser.parse_args()

    viz = CovidVisualization(args.csv, args.out)

    # Generate all required charts
    viz.bar_top10_confirmed()
    viz.pie_deaths_by_region()
    viz.line_confirmed_vs_deaths_top5()
    viz.scatter_confirmed_vs_recovered()
    viz.hist_deaths_all_regions()
    viz.stacked_bar_selected_countries()
    viz.boxplot_confirmed_by_region()
    viz.trendline_india_vs(args.other)

    print("\nAll charts generated successfully.")


if __name__ == "__main__":
    main()
