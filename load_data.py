import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# --- 1. Load data ---
# skiprows=1 because the first row of the CSV is just a title, not the header
df = pd.read_csv(
    "/Users/isabellafrommherz/PycharmProjects/climate-data-analysis/data:/GLB.Ts+dSST.csv",
    skiprows=1
)

# --- 2. Clean data ---
# The "J-D" column contains "***" for missing values, so it gets read in as strings.
# errors="coerce" turns "***" into NaN instead of raising an error.
df["J-D"] = pd.to_numeric(df["J-D"], errors="coerce")

# Keep only the relevant columns: year and annual mean temperature anomaly
annual_df = df[["Year", "J-D"]]

# Drop rows with missing values (e.g. very early years without complete data)
annual_df = annual_df.dropna()

# --- 3. Linear regression model ---
# X needs to be 2D (sklearn convention), hence [["Year"]] instead of ["Year"]
X = annual_df[["Year"]]
y = annual_df["J-D"]

model = LinearRegression()
model.fit(X, y)

# coef_[0] to print the slope as a single number instead of an array
print(f"Slope (°C per year): {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.2f}")

# Compute predictions
y_pred = model.predict(X)

# --- 4. Visualization: two plots in one figure ---
fig, axes = plt.subplots(2, 1, figsize=(8, 8))  # 2 rows, 1 column

# First plot: actual data only
axes[0].plot(annual_df["Year"], annual_df["J-D"])
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Temperature Anomaly (°C)")
axes[0].set_title("Global Annual Mean Temperature Anomaly Over Time")

# Second plot: actual data + regression
axes[1].plot(X, y, label="Actual")
axes[1].plot(X, y_pred, label="Linear Regression", linestyle="--")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Temperature Anomaly (°C)")
axes[1].set_title("Actual vs. Predicted Annual Mean Temperature Anomaly")
axes[1].legend()

plt.tight_layout()  # prevents titles/labels from overlapping

plt.savefig("output.png", dpi=150, bbox_inches="tight")
plt.show()

plt.show()