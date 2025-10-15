import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def pick_column(name_candidates, cols_norm_map):
    for norm_name, orig in cols_norm_map.items():
        for cand in name_candidates:
            if cand in norm_name:
                return orig
    return None

def main(csv_path="house_price_regression_dataset.csv"):
    df = pd.read_csv(csv_path)

    norm_map = {c.strip().lower().replace("-", " ").replace("_", " "): c for c in df.columns}

    square_candidates = [
        "square footage", "squarefootage", "square feet", "sqft", "sq ft", "area", "size", "living area", "living space"
    ]
    price_candidates = [
        "price", "sale price", "sold price", "listing price", "cost", "amount"
    ]

    square_col = pick_column(square_candidates, norm_map)
    price_col = pick_column(price_candidates, norm_map)

    if square_col is None and "Square Footage" in df.columns:
        square_col = "Square Footage"
    if price_col is None and "Price" in df.columns:
        price_col = "Price"

    if square_col is None or price_col is None:
        raise ValueError(f"Could not identify required columns in {list(df.columns)}")

    data = df[[square_col, price_col]].copy()
    data.dropna(subset=[square_col, price_col], inplace=True)

    X = data[[square_col]].values
    y = data[price_col].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = float(np.sqrt(mse))
    r2 = r2_score(y_test, y_pred)

    print("Intercept (b0):", float(model.intercept_))
    print("Coefficient (b1):", float(model.coef_[0]))
    print("MSE:", float(mse))
    print("RMSE:", float(rmse))
    print("R^2:", float(r2))

    # Save figures
    x_line = np.linspace(data[square_col].min(), data[square_col].max(), 200).reshape(-1, 1)
    y_line = model.predict(x_line)

    plt.figure()
    plt.scatter(data[square_col], data[price_col])
    plt.plot(x_line, y_line)
    plt.xlabel(square_col); plt.ylabel(price_col)
    plt.title("Linear Regression: Price vs Square Footage")
    plt.savefig("regression_line_plot.png", bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.scatter(y_test, y_pred)
    min_val = min(np.min(y_test), np.min(y_pred))
    max_val = max(np.max(y_test), np.max(y_pred))
    plt.plot([min_val, max_val], [min_val, max_val])
    plt.xlabel("Actual Price (Test)"); plt.ylabel("Predicted Price")
    plt.title("Actual vs Predicted Prices (Test Set)")
    plt.savefig("actual_vs_predicted.png", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()