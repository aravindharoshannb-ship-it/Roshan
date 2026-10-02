import pandas as pd
import numpy as np
import os

# ============================================================
# 1. File paths
# ============================================================

INPUT_FILE = "C:\Users\aravi\OneDrive\Desktop\Disaster_NLP_Intelligent_System/dataset/public_emdat_project.csv"
OUTPUT_FILE = "C:\Users\aravi\OneDrive\Desktop\Disaster_NLP_Intelligent_System/dataset/cleaned_disaster_data.csv"

# ============================================================
# 2. Load dataset
# ============================================================

print("Loading disaster dataset...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="latin1",
    low_memory=False
)

print("\nDataset loaded successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# ============================================================
# 3. Remove duplicate records
# ============================================================

before = len(df)

df = df.drop_duplicates()

after = len(df)

print("\nDuplicate records removed:", before - after)

# ============================================================
# 4. Convert important numeric columns
# ============================================================

numeric_columns = [
    "Start Year",
    "Start Month",
    "Start Day",
    "End Year",
    "End Month",
    "End Day",
    "Total Deaths",
    "No. Injured",
    "No. Affected",
    "No. Homeless",
    "Total Affected",
    "Latitude",
    "Longitude",
    "Magnitude",
    "Total Damage ('000 US$)"
]

for column in numeric_columns:

    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

# ============================================================
# 5. Fill text missing values
# ============================================================

text_columns = [
    "Country",
    "Region",
    "Subregion",
    "Location",
    "Disaster Group",
    "Disaster Subgroup",
    "Disaster Type",
    "Disaster Subtype",
    "Event Name",
    "Origin",
    "Associated Types"
]

for column in text_columns:

    if column in df.columns:
        df[column] = df[column].fillna("Unknown")

# ============================================================
# 6. Create disaster date
# ============================================================

df["Start Date"] = pd.to_datetime(
    dict(
        year=df["Start Year"],
        month=df["Start Month"].fillna(1),
        day=df["Start Day"].fillna(1)
    ),
    errors="coerce"
)

# ============================================================
# 7. Create severity level
# ============================================================

def calculate_severity(row):

    deaths = row["Total Deaths"]
    affected = row["Total Affected"]
    damage = row["Total Damage ('000 US$)"]

    deaths = 0 if pd.isna(deaths) else deaths
    affected = 0 if pd.isna(affected) else affected
    damage = 0 if pd.isna(damage) else damage

    if deaths >= 100 or affected >= 100000 or damage >= 100000:
        return "High"

    elif deaths >= 10 or affected >= 10000 or damage >= 10000:
        return "Medium"

    else:
        return "Low"


df["Severity"] = df.apply(
    calculate_severity,
    axis=1
)

# ============================================================
# 8. Create NLP training text
# ============================================================

df["Disaster Text"] = (
    "Disaster: " +
    df["Disaster Type"].astype(str) +
    ". Location: " +
    df["Location"].astype(str) +
    ". Country: " +
    df["Country"].astype(str) +
    ". Event: " +
    df["Event Name"].astype(str) +
    ". Deaths: " +
    df["Total Deaths"].fillna(0).astype(int).astype(str) +
    ". Affected: " +
    df["Total Affected"].fillna(0).astype(int).astype(str) +
    ". Severity: " +
    df["Severity"].astype(str)
)

# ============================================================
# 9. Save cleaned dataset
# ============================================================

os.makedirs("dataset", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print("\nCleaned dataset saved successfully:")
print(OUTPUT_FILE)

# ============================================================
# 10. Display summary
# ============================================================

print("\n========== DATASET SUMMARY ==========")

print("Total records:", len(df))
print("Total columns:", len(df.columns))

print("\nDisaster Types:")
print(
    df["Disaster Type"]
    .value_counts()
    .head(15)
)

print("\nSeverity Distribution:")
print(
    df["Severity"]
    .value_counts()
)

print("\nTop Countries:")
print(
    df["Country"]
    .value_counts()
    .head(10)
)

print("\nProcessing completed!")
