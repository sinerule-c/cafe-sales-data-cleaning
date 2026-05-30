# Import libraries and load the CSV
import pandas as pd
import numpy as np

df = pd.read_csv("dirty_cafe_sales.csv")

# Clean column names
df.columns = (
    df.columns
    .str.strip()            # remove extra spaces at the front/back of column names
    .str.lower()            # make all column names lowercase
    .str.replace(" ", "_")  # replace spaces inside column names with underscores
)

# Remove extra spaces in text
df = df.apply(lambda col: col.str.strip() if col.dtype == ("object", "str", "string") else col)

# Meaning:
# - apply() checks each column one by one
# - if the column is text, strip spaces
# - otherwise, return the column unchanged

# Check column names, number of rows, missing values, and data types
df.info()

# Replace NaN with Unknown
df["item"] = df["item"].fillna("Unknown").replace(("UNKNOWN","ERROR"), "Unknown")
df["item"].value_counts()

df["payment_method"] = df["payment_method"].fillna("Unknown").replace(("UNKNOWN", "ERROR"), "Unknown")
df["payment_method"].value_counts()

df["location"] = df["location"].fillna("Unknown").replace(("UNKNOWN", "ERROR"), "Unknown")
df["location"].value_counts()

# Price of Cake = 3.0
df[df["item"] == "Cake"]["price_per_unit"].value_counts(dropna=False)

# Price of Coffee = 2.0
df[df["item"] == "Coffee"]["price_per_unit"].value_counts(dropna=False)

# Price of Cookie = 1.0
df[df["item"] == "Cookie"]["price_per_unit"].value_counts(dropna=False)

# Price of Juice = 3.0
df[df["item"] == "Juice"]["price_per_unit"].value_counts(dropna=False)

# Price of Salad = 5.0
df[df["item"] == "Salad"]["price_per_unit"].value_counts(dropna=False)

# Price of Sandwich = 4.0
df[df["item"] == "Sandwich"]["price_per_unit"].value_counts(dropna=False)

# Price of Smoothie = 4.0
df[df["item"] == "Smoothie"]["price_per_unit"].value_counts(dropna=False)

# Price of Tea = 1.5
df[df["item"] == "Tea"]["price_per_unit"].value_counts(dropna=False)

df["price_per_unit"] = pd.to_numeric(df["price_per_unit"], errors="coerce")

# Fill missing item prices
df.loc[(df["item"]== "Cake") & (df["price_per_unit"].isna()), "price_per_unit"] = 3.0
df.loc[(df["item"]== "Coffee") & (df["price_per_unit"].isna()), "price_per_unit"] = 2.0
df.loc[(df["item"]== "Cookie") & (df["price_per_unit"].isna()), "price_per_unit"] = 1.0
df.loc[(df["item"]== "Juice") & (df["price_per_unit"].isna()), "price_per_unit"] = 3.0
df.loc[(df["item"]== "Salad") & (df["price_per_unit"].isna()), "price_per_unit"] = 5.0
df.loc[(df["item"]== "Sandwich") & (df["price_per_unit"].isna()), "price_per_unit"] = 4.0
df.loc[(df["item"]== "Smoothie") & (df["price_per_unit"].isna()), "price_per_unit"] = 4.0
df.loc[(df["item"]== "Tea") & (df["price_per_unit"].isna()), "price_per_unit"] = 1.5

# Validate prices after filling
df.groupby("item")["price_per_unit"].value_counts(dropna=False)

# Fill missing item based on price_per_unit
# We do NOT fill 3.0 because it could be Cake or Juice.
# We do NOT fill 4.0 because it could be Sandwich or Smoothie.
df.loc[(df["item"] == "Unknown") & (df["price_per_unit"] == 1.5), "item"] = "Tea"
df.loc[(df["item"] == "Unknown") & (df["price_per_unit"] == 1.0), "item"] = "Cookie"
df.loc[(df["item"] == "Unknown") & (df["price_per_unit"] == 5.0), "item"] = "Salad"
df.loc[(df["item"] == "Unknown") & (df["price_per_unit"] == 2.0), "item"] = "Coffee"

# Check item-price again
df.groupby("item")["price_per_unit"].value_counts(dropna=False)

# Convert to_numeric, fill with NaN
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["total_spent"] = pd.to_numeric(df["total_spent"], errors="coerce")

# Get total_spent using formula quantity * price_per_unit
df["total_spent"] = df["total_spent"].fillna(df["quantity"] * df["price_per_unit"])

# Get quantity using formula total_spent/price_per_unit
df["quantity"] = df["quantity"].fillna(df["total_spent"]/ df["price_per_unit"])

# Get price_per_unit using formula total_spent/quantity
df["price_per_unit"] = df["price_per_unit"].fillna(df["total_spent"]/ df["quantity"])

# Convert transaction_date into a real datetime column
df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

# Inspect the cleaned dataset
df.info()

# Filter rows with unknown
df[
    (df["item"] == "Unknown") |
    (df["payment_method"] == "Unknown") |
    (df["location"] == "Unknown")
]

df.to_csv("cleaned_cafe_sales.csv", index=False)