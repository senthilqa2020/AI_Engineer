# covid_eda.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from pathlib import Path


class CovidEDA:
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self.df = None
        self.df_clean = None
        self.df_scaled = None
        self.scaler = None
        # canonical column names we’ll keep
        self.cols = ["Confirmed", "New cases"]

    def load_and_prepare(self):
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV not found: {self.csv_path.resolve()}")
        df = pd.read_csv(self.csv_path)

        # Try to normalize likely column name variants
        rename_map = {}
        for c in df.columns:
            lc = c.strip().lower()
            if lc in {"confirmed", "confirmedcases", "totalconfirmed"}:
                rename_map[c] = "Confirmed"
            if lc in {"new cases", "newcases", "new_case", "new_case(s)", "new"}:
                rename_map[c] = "New cases"
        df = df.rename(columns=rename_map)

        missing = [c for c in self.cols if c not in df.columns]
        if missing:
            raise KeyError(
                f"Required columns missing: {missing}. "
                f"Found columns: {sorted(df.columns.tolist())}"
            )

        # Keep only target columns & coerce to numeric
        df = df[self.cols].apply(pd.to_numeric, errors="coerce")
        # Drop rows that are completely NA on both columns
        df = df.dropna(how="all", subset=self.cols).reset_index(drop=True)
        self.df = df
        return self.df

    def compute_statistics(self):
        if self.df is None:
            raise ValueError("Call load_and_prepare() first.")

        stats = {
            "mean": self.df[self.cols].mean().to_dict(),
            "median": self.df[self.cols].median().to_dict(),
            "variance": self.df[self.cols].var(ddof=1).to_dict(),
            "std_dev": self.df[self.cols].std(ddof=1).to_dict(),
            "correlation_matrix": self.df[self.cols].corr().round(4),
        }

        print("\n=== Descriptive Statistics ===")
        for k in ["mean", "median", "variance", "std_dev"]:
            print(k.capitalize(), {c: round(v, 4) for c, v in stats[k].items()})
        print("\nCorrelation Matrix:\n", stats["correlation_matrix"])
        return stats

    def _iqr_bounds(self, series: pd.Series):
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        return lower, upper

    def remove_outliers_iqr(self):
        if self.df is None:
            raise ValueError("Call load_and_prepare() first.")

        mask = pd.Series(True, index=self.df.index)
        outlier_counts = {}

        for col in self.cols:
            lower, upper = self._iqr_bounds(self.df[col].dropna())
            col_mask = self.df[col].between(lower, upper, inclusive="both")
            outlier_counts[col] = int((~col_mask).sum())
            mask &= col_mask.fillna(False)  # treat NaNs as outliers to be safe

        df_clean = self.df[mask].reset_index(drop=True)
        self.df_clean = df_clean

        print("\n=== IQR Outlier Detection ===")
        for col in self.cols:
            print(f"Outliers in {col}: {outlier_counts[col]}")
        print("\nCleaned dataset (first 10 rows):")
        print(df_clean.head(10))
        return df_clean, outlier_counts

    def normalize_with_standard_scaler(self, use_cleaned=True):
        if use_cleaned:
            if self.df_clean is None:
                raise ValueError("Call remove_outliers_iqr() first.")
            data = self.df_clean[self.cols]
        else:
            if self.df is None:
                raise ValueError("Call load_and_prepare() first.")
            data = self.df[self.cols]

        scaler = StandardScaler()
        scaled = scaler.fit_transform(data.values)
        df_scaled = pd.DataFrame(scaled, columns=self.cols, index=data.index)

        self.scaler = scaler
        self.df_scaled = df_scaled

        print("\n=== StandardScaler Normalization ===")
        print(df_scaled.head(10))
        return df_scaled, scaler

    def plot_histograms(self, before=True, after=True):
        if before and self.df is None:
            raise ValueError("Call load_and_prepare() first.")
        if after and self.df_scaled is None:
            raise ValueError("Call normalize_with_standard_scaler() first.")

        if before:
            plt.figure()
            sns.histplot(self.df["Confirmed"].dropna(), kde=True)
            plt.title("Confirmed (Before Normalization)")
            plt.xlabel("Confirmed")
            plt.ylabel("Count")
            plt.tight_layout()

            plt.figure()
            sns.histplot(self.df["New cases"].dropna(), kde=True)
            plt.title("New cases (Before Normalization)")
            plt.xlabel("New cases")
            plt.ylabel("Count")
            plt.tight_layout()

        if after:
            plt.figure()
            sns.histplot(self.df_scaled["Confirmed"].dropna(), kde=True)
            plt.title("Confirmed (After StandardScaler)")
            plt.xlabel("Confirmed (z-score)")
            plt.ylabel("Count")
            plt.tight_layout()

            plt.figure()
            sns.histplot(self.df_scaled["New cases"].dropna(), kde=True)
            plt.title("New cases (After StandardScaler)")
            plt.xlabel("New cases (z-score)")
            plt.ylabel("Count")
            plt.tight_layout()

        plt.show()

    def plot_heatmap(self, use_cleaned=True):
        if use_cleaned:
            if self.df_clean is None:
                raise ValueError("Call remove_outliers_iqr() first.")
            corr = self.df_clean[self.cols].corr()
            title = "Correlation Heatmap (Cleaned)"
        else:
            if self.df is None:
                raise ValueError("Call load_and_prepare() first.")
            corr = self.df[self.cols].corr()
            title = "Correlation Heatmap (Raw)"

        plt.figure()
        sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, square=True)
        plt.title(title)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # Path to your CSV
    CSV_PATH = "country_wise_latest.csv"

    eda = CovidEDA(CSV_PATH)
    eda.load_and_prepare()
    eda.compute_statistics()
    eda.remove_outliers_iqr()
    eda.normalize_with_standard_scaler(use_cleaned=True)

    # Visualizations
    eda.plot_histograms(before=True, after=True)
    eda.plot_heatmap(use_cleaned=True)
