# Cafe Sales Data Cleaning Project

## Project Overview

This project focuses on cleaning a messy cafe sales dataset using Python and Pandas.

The goal of this project is to understand how real-world datasets can contain missing values, inconsistent text, wrong data types, and invalid entries.

This project includes:

* Loading a dataset
* Cleaning column names
* Removing extra spaces from text
* Checking missing values and data types
* Replacing invalid values such as `UNKNOWN` and `ERROR`
* Filling missing item prices
* Filling missing item names where possible
* Converting columns to the correct data type
* Calculating missing `total_spent`
* Calculating missing `quantity`
* Calculating missing `price_per_unit`
* Converting transaction dates into datetime format
* Filtering rows with unknown values
* Exporting the cleaned dataset

## Dataset

The dataset used is `dirty_cafe_sales.csv`.

It contains cafe sales transaction data.

The dataset has 10,000 rows and 8 columns.

Main columns used:

| Column           | Description                                |
| ---------------- | ------------------------------------------ |
| transaction_id   | Unique transaction ID                      |
| item             | Item purchased by the customer             |
| quantity         | Number of items purchased                  |
| price_per_unit   | Price of one unit of the item              |
| total_spent      | Total amount spent by the customer         |
| payment_method   | Payment method used                        |
| location         | Whether the order was takeaway or in-store |
| transaction_date | Date of the transaction                    |

## Tools and Libraries Used

This project was done using Python.

Libraries used:

```python
import pandas as pd
import numpy as np
```

## Data Cleaning Process

### 1. Loading the Dataset

The dataset was loaded using Pandas.

```python
df = pd.read_csv("dirty_cafe_sales.csv")
```

This allowed the CSV file to be stored as a DataFrame so that it could be cleaned and analysed using Python.

---

### 2. Cleaning Column Names

The column names were cleaned by:

* Removing extra spaces
* Changing all column names to lowercase
* Replacing spaces with underscores

```python
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)
```

This makes the column names easier to work with in Python.

For example:

```text
Transaction ID → transaction_id
Price Per Unit → price_per_unit
Total Spent → total_spent
```

---

### 3. Removing Extra Spaces in Text

Extra spaces were removed from text columns.

```python
df = df.apply(lambda col: col.str.strip() if col.dtype == ("object", "str", "string") else col)
```

This helps prevent problems where values look the same but are actually different because of hidden spaces.

For example:

```text
" Coffee " → "Coffee"
```

---

### 4. Checking the Dataset

The dataset was checked using:

```python
df.info()
```

This was used to inspect:

* Number of rows
* Number of columns
* Missing values
* Data types

Before cleaning, all columns were stored as string data types.

Some columns also had missing values, such as:

* `item`
* `quantity`
* `price_per_unit`
* `total_spent`
* `payment_method`
* `location`
* `transaction_date`

---

### 5. Cleaning Item, Payment Method, and Location

Missing values in `item`, `payment_method`, and `location` were replaced with `Unknown`.

Invalid values such as `UNKNOWN` and `ERROR` were also replaced with `Unknown`.

```python
df["item"] = df["item"].fillna("Unknown").replace(("UNKNOWN","ERROR"), "Unknown")

df["payment_method"] = df["payment_method"].fillna("Unknown").replace(("UNKNOWN", "ERROR"), "Unknown")

df["location"] = df["location"].fillna("Unknown").replace(("UNKNOWN", "ERROR"), "Unknown")
```

This makes the data more consistent.

For example:

```text
UNKNOWN → Unknown
ERROR → Unknown
NaN → Unknown
```

---

### 6. Checking Item Prices

The price of each item was checked using `value_counts()`.

For example:

```python
df[df["item"] == "Cake"]["price_per_unit"].value_counts(dropna=False)
```

This was done for each item to identify the correct price.

The item prices found were:

| Item     | Price Per Unit |
| -------- | -------------: |
| Cake     |            3.0 |
| Coffee   |            2.0 |
| Cookie   |            1.0 |
| Juice    |            3.0 |
| Salad    |            5.0 |
| Sandwich |            4.0 |
| Smoothie |            4.0 |
| Tea      |            1.5 |

---

### 7. Converting Price Per Unit to Numeric

The `price_per_unit` column was converted into a numeric column.

```python
df["price_per_unit"] = pd.to_numeric(df["price_per_unit"], errors="coerce")
```

`errors="coerce"` changes invalid values such as `ERROR` and `UNKNOWN` into missing values.

This makes it possible to fill or calculate the missing prices later.

---

### 8. Filling Missing Item Prices

Missing item prices were filled based on the known price of each item.

```python
df.loc[(df["item"]== "Cake") & (df["price_per_unit"].isna()), "price_per_unit"] = 3.0
df.loc[(df["item"]== "Coffee") & (df["price_per_unit"].isna()), "price_per_unit"] = 2.0
df.loc[(df["item"]== "Cookie") & (df["price_per_unit"].isna()), "price_per_unit"] = 1.0
df.loc[(df["item"]== "Juice") & (df["price_per_unit"].isna()), "price_per_unit"] = 3.0
df.loc[(df["item"]== "Salad") & (df["price_per_unit"].isna()), "price_per_unit"] = 5.0
df.loc[(df["item"]== "Sandwich") & (df["price_per_unit"].isna()), "price_per_unit"] = 4.0
df.loc[(df["item"]== "Smoothie") & (df["price_per_unit"].isna()), "price_per_unit"] = 4.0
df.loc[(df["item"]== "Tea") & (df["price_per_unit"].isna()), "price_per_unit"] = 1.5
```

This improved the quality of the dataset by replacing missing prices with logical values.

---

### 9. Filling Missing Item Names Based on Price

Some item names were unknown, but their price was available.

For items with unique prices, the missing item names were filled.

```python
df.loc[(df["item"] == "Unknown") & (df["price_per_unit"] == 1.5), "item"] = "Tea"
df.loc[(df["item"] == "Unknown") & (df["price_per_unit"] == 1.0), "item"] = "Cookie"
df.loc[(df["item"] == "Unknown") & (df["price_per_unit"] == 5.0), "item"] = "Salad"
df.loc[(df["item"] == "Unknown") & (df["price_per_unit"] == 2.0), "item"] = "Coffee"
```

However, some prices were shared by more than one item.

For example:

| Price | Possible Items       |
| ----: | -------------------- |
|   3.0 | Cake or Juice        |
|   4.0 | Sandwich or Smoothie |

Because these prices could belong to more than one item, they were not filled to avoid guessing wrongly.

---

### 10. Calculating Missing Total Spent

The `quantity` and `total_spent` columns were converted into numeric columns.

```python
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["total_spent"] = pd.to_numeric(df["total_spent"], errors="coerce")
```

Missing `total_spent` values were calculated using:

```python
df["total_spent"] = df["total_spent"].fillna(df["quantity"] * df["price_per_unit"])
```

Formula used:

```text
total_spent = quantity × price_per_unit
```

---

### 11. Calculating Missing Quantity and Price Per Unit

Missing `quantity` values were calculated using:

```python
df["quantity"] = df["quantity"].fillna(df["total_spent"] / df["price_per_unit"])
```

Formula used:

```text
quantity = total_spent ÷ price_per_unit
```

Missing `price_per_unit` values were calculated using:

```python
df["price_per_unit"] = df["price_per_unit"].fillna(df["total_spent"] / df["quantity"])
```

Formula used:

```text
price_per_unit = total_spent ÷ quantity
```

---

### 12. Converting Transaction Date

The `transaction_date` column was converted into datetime format.

```python
df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
```

This allows the date column to be used properly for time-based analysis in the future.

Invalid dates were converted into missing values.

---

### 13. Inspecting the Cleaned Dataset

After cleaning, the dataset was checked again using:

```python
df.info()
```

After cleaning:

* `transaction_id` had 10,000 non-null values
* `item` had 10,000 non-null values
* `payment_method` had 10,000 non-null values
* `location` had 10,000 non-null values
* `quantity` had 9,977 non-null values
* `price_per_unit` had 9,994 non-null values
* `total_spent` had 9,977 non-null values
* `transaction_date` had 9,540 non-null values

The data types were also improved:

| Column           | Cleaned Data Type |
| ---------------- | ----------------- |
| transaction_id   | string            |
| item             | string            |
| quantity         | float             |
| price_per_unit   | float             |
| total_spent      | float             |
| payment_method   | string            |
| location         | string            |
| transaction_date | datetime          |

---

### 14. Filtering Rows with Unknown Values

Rows with unknown values were filtered using:

```python
df[
    (df["item"] == "Unknown") |
    (df["payment_method"] == "Unknown") |
    (df["location"] == "Unknown")
]
```

This helps identify rows that still have incomplete or uncertain information after cleaning.

---

### 15. Exporting the Cleaned Dataset

The cleaned dataset was saved as a new CSV file.

```python
df.to_csv("cleaned_cafe_sales.csv", index=False)
```

The cleaned file is:

```text
cleaned_cafe_sales.csv
```

`index=False` prevents Pandas from saving the DataFrame index as an extra column.

## Data Cleaning Summary

Before cleaning, the dataset had many issues, such as:

* Messy column names
* Extra spaces in text
* Missing values
* Invalid values like `UNKNOWN` and `ERROR`
* Numeric columns stored as text
* Invalid transaction dates
* Missing item names
* Missing prices
* Missing quantity and total spent values

After cleaning, the dataset became more consistent and easier to use for analysis.

Key cleaning actions included:

* Standardising column names
* Replacing invalid text values with `Unknown`
* Filling missing prices using known item prices
* Filling some missing item names using price information
* Calculating missing `total_spent`
* Calculating missing `quantity`
* Calculating missing `price_per_unit`
* Converting `transaction_date` into datetime format
* Exporting the cleaned data into a new CSV file

## What I Learned

Through this project, I learned how to:

* Load a CSV dataset using Pandas
* Clean messy column names
* Remove extra spaces from text data
* Check missing values and data types using `df.info()`
* Replace missing and invalid values
* Use `value_counts()` to understand item-price patterns
* Convert columns into numeric data types using `pd.to_numeric()`
* Use `errors="coerce"` to handle invalid numeric values
* Fill missing values using logical rules
* Calculate missing values using formulas
* Convert dates using `pd.to_datetime()`
* Filter rows based on conditions
* Export a cleaned DataFrame to a new CSV file

## Conclusion

This project shows how important data cleaning is before doing data analysis or machine learning.

The original cafe sales dataset contained missing values, invalid text values, incorrect data types, and incomplete transaction information. By cleaning the dataset step by step, the data became more reliable and easier to work with.

The project also helped me understand that not every missing value should be guessed. For example, item names with prices of 3.0 and 4.0 were left as `Unknown` because those prices could belong to more than one item. This avoids making incorrect assumptions.

Overall, this is a useful beginner data cleaning project because it focuses on real-world data problems such as missing values, inconsistent labels, wrong data types, and calculated fields. The cleaned dataset can now be used for further analysis, visualisation, or machine learning in the future.
