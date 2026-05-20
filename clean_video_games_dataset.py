import pandas as pd
import numpy as np

# Load original dataset
df = pd.read_csv("Video_Games_Sales_as_at_22_Dec_2016.csv")

# Remove duplicate rows
df = df.drop_duplicates()

# Replace "tbd" with NaN
df["User_Score"] = df["User_Score"].replace("tbd", np.nan)

# Convert columns to numeric
numeric_columns = [
    "Year_of_Release",
    "NA_Sales",
    "EU_Sales",
    "JP_Sales",
    "Other_Sales",
    "Global_Sales",
    "Critic_Score",
    "Critic_Count",
    "User_Score",
    "User_Count",
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows missing important values
df = df.dropna(subset=[
    "Name",
    "Platform",
    "Genre",
    "Year_of_Release",
    "Global_Sales"
])

# Fill missing categorical values
df["Publisher"] = df["Publisher"].fillna("Unknown")
df["Developer"] = df["Developer"].fillna("Unknown")
df["Rating"] = df["Rating"].fillna("Not Rated")

# Fill missing review values using median
review_cols = ["Critic_Score", "Critic_Count", "User_Score", "User_Count"]

for col in review_cols:
    df[col] = df[col].fillna(df[col].median())

# Convert release year to integer
df["Year_of_Release"] = df["Year_of_Release"].astype(int)

# Remove impossible years
df = df[(df["Year_of_Release"] >= 1980) & (df["Year_of_Release"] <= 2016)]

# Sort values
df = df.sort_values(by=["Year_of_Release", "Global_Sales"], ascending=[True, False])

# Reset index
df = df.reset_index(drop=True)

# Save cleaned dataset
df.to_csv("video_games_sales_cleaned.csv", index=False)

print("Dataset cleaned successfully!")
