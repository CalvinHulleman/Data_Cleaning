# ama_age_visualizations.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

df = pd.read_csv("ama_clean.csv")
df["Exit Year"] = pd.to_numeric(df["Exit Year"], errors="coerce")
df["Other No"] = pd.to_numeric(df["Other No"], errors="coerce")
df["Birth Year"] = pd.to_numeric(df["Birth Year"], errors="coerce")
df["ExitYear"] = df["Exit Year"].fillna(df["Other No"])

df["AgeAtExit"] = df["ExitYear"] - df["Birth Year"]
df_clean = df.dropna(subset=["ExitYear", "Birth Year", "AgeAtExit"]).copy()
df_clean = df_clean[(df_clean["AgeAtExit"] >= 9) & (df_clean["AgeAtExit"] <= 100)]

# Histogram of ages
plt.figure(figsize=(10, 6))
plt.hist(df_clean["AgeAtExit"], bins=range(10, 61), color="lightgreen", edgecolor="black")
plt.xlabel("Age at Exit (years)")
plt.ylabel("Number of Students")
plt.title("Distribution of Age at Exit")
plt.tight_layout()
plt.savefig("age_histogram.png", dpi=150)
plt.close()

print(df_clean["AgeAtExit"].median())