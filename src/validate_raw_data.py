from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# Generate a list of files to validate
files = [
    "sales_jan.xlsx",
    "sales_feb.xlsx",
    "sales_mar.xlsx",
    "sales_apr.xlsx",
    "sales_may.xlsx",
    "sales_june.xlsx",
    "sales_july.xlsx",
    "sales_aug.xlsx",
    "sales_sept.xlsx"
]

# Column name mapping
col_mapping = {
    "order_id": "order_id",
    "Order ID": "order_id",
    "OrderID": "order_id",
}

total_rows = 0
total_duplicate = 0
total_blank_rows = 0
total_missing_values = 0

# Validate each file
for file_name in files:

    file_path = RAW_DATA_DIR / file_name

    print("=" * 70)
    print(f"FILE: {file_name}")
    print("=" * 70)

    if not file_path.exists():
        print("ERROR: File does not exist.")
        continue

    df = pd.read_excel(file_path)

    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    order_id_col = None
    for col in df.columns:
        normalized_col = (col.strip().lower().replace("_", "").replace(" ", ""))
        if normalized_col in ["orderid", "ordernumber"]:
            order_id_col = col
            break

    # Check for duplicate Order IDs
    if order_id_col:
        duplicate_orders = df[order_id_col].duplicated().sum()

        print(f"Order ID Column: {order_id_col}")
        print(f"Duplicate Order IDs: {duplicate_orders}")

        total_duplicate += duplicate_orders

    else:
        print("Order ID Column: Not found in this file.")


    # Check for completely blank rows
    blank_rows = df.isna().all(axis=1).sum()

    print(f"Completely blank rows: {blank_rows}")

    # Check for missing values in the entire DataFrame
    missing_values = df.isna().sum().sum()

    print(f"Missing values: {missing_values}")

    total_rows += len(df)
    total_blank_rows += blank_rows
    total_missing_values += missing_values


# Print summary across all files
print("\n" + "=" * 70)
print("SUMMARY ACROSS ALL FILES")
print("=" * 70)
print(f"TOTAL ROWS ACROSS ALL FILES: {total_rows}")
print(f"TOTAL DUPLICATE ORDER IDs ACROSS ALL FILES: {total_duplicate}")
print(f"TOTAL BLANK ROWS ACROSS ALL FILES: {total_blank_rows}")
print(f"TOTAL MISSING VALUES ACROSS ALL FILES: {total_missing_values}")

print("=" * 70)


