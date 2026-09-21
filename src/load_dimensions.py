import psycopg2
import os
import sys
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RAW_DATA = Path("data/raw")
PROCESSED_FILE = Path("data/processed_files.txt")

all_files = sorted(
    file.name
    for file in RAW_DATA.glob("*.xlsx")
)

processed_files = set()

if PROCESSED_FILE.exists():
    with open(PROCESSED_FILE, "r") as file:
        processed_files = {
            line.strip()
            for line in file
            if line.strip()
        }

if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = [
        file
        for file in all_files
        if file not in processed_files
]

print("\nINPUT FILE CHECK")
print("----------------")
print("Files found:", len(all_files))
print("Already processed:", len(processed_files))
print("New files:", len(files))

for file in files:
    print("-", file)

if not files:
    print("No new files to process.")
    exit()

dataframes = []

for file in files:
    df = pd.read_excel(RAW_DATA / file)
    dataframes.append(df)

# =========================
# LOAD DIM_CUSTOMER
# =========================

customer_columns = {
    "Customer_ID": "customer_id",
    "Customer Id": "customer_id",
    "CustomerID": "customer_id",
    "Customer_code": "customer_id",
    "Customer code": "customer_id",
    "Customer Code": "customer_id",
    "Customer ID": "customer_id",
    "customer_id": "customer_id",
    "Customer_id": "customer_id",
    "Customer": "customer_id",

    "Customer_Name": "customer_name",
    "Customer Name": "customer_name",
    "CustomerName": "customer_name",
    "Customer NAME": "customer_name",
    "customer_name": "customer_name",
    "Customer_name": "customer_name"
    
}

for df in dataframes:
    df.rename(columns=customer_columns, inplace=True)

customer_data = []

for df in dataframes:
    customer_data.append(
        df[["customer_id", "customer_name"]]
    )

customers = pd.concat(customer_data, ignore_index=True)

# Keep one record per customer
customers = customers.drop_duplicates(subset=["customer_id"])

#Remove records with missing customer ID
customers = customers.dropna(subset=["customer_id"])

# Validation
print("\nCUSTOMER VALIDATION")
print(f"Unique customers: {len(customers)}")
print(f"Missing customer IDs: {customers['customer_id'].isna().sum()}")
print(f"Missing customer names: {customers['customer_name'].isna().sum()}")
print(f"Duplicate customer IDs: {customers['customer_id'].duplicated().sum()}")
print(customers.head(10))

# =========================
# LOAD DIM_PRODUCT
# =========================

product_columns = {
    "Product_ID": "product_id",
    "Product Id": "product_id",
    "ProductID": "product_id",
    "Product": "product_id",
    "Item_code": "product_id",
    "Item Code": "product_id",
    "Product_code": "product_id",
    "Product Code": "product_id",

    "Product_Name": "product_name",
    "Product Name": "product_name",
    "Item Name": "product_name",

    "Unit_Price": "unit_price",
    "Unit Price": "unit_price",
    "UnitPrice": "unit_price",
    "Price": "unit_price",
    "Price Per Unit": "unit_price",
    "Unit Cost": "unit_price"
}

product_data = []

for df in dataframes:
    df.rename(columns=product_columns, inplace=True)

for df in dataframes:
    product_data.append(
        df[["product_id", "product_name", "unit_price"]]
    )

products = pd.concat(product_data, ignore_index=True)

# Remove records with missing product ID
products = products.dropna(subset=["product_id"])

# Keep one record per product
products = products.drop_duplicates(subset=["product_id"])

# Validation
print("\nPRODUCT VALIDATION")
print("Unique products:", len(products))
print("Missing product IDs:", products["product_id"].isna().sum())
print("Missing product names:", products["product_name"].isna().sum())
print("Duplicate product IDs:", products["product_id"].duplicated().sum())
print(products)


# =========================
# LOAD DIM_REGION
# =========================

region_data = []

for df in dataframes:
    region_data.append(
        df[["Region"]]
        )

regions = pd.concat(region_data, ignore_index=True)

# Remove missing regions
regions = regions.dropna(subset=["Region"])

# Keep one record per region
regions = regions.drop_duplicates(subset=["Region"])

# Rename column
regions.rename(
    columns={"Region": "region_name"},
    inplace=True
)

print("\nREGION VALIDATION")
print("Unique regions:", len(regions))
print("Missing regions:", regions["region_name"].isna().sum())
print("Duplicate regions:", regions["region_name"].duplicated().sum())
print(regions)


# =========================
# PREPARE FACT_SALES
# =========================

sales_columns = {
    # Order
    "Order_ID": "order_id",
    "Order ID": "order_id",
    "OrderID": "order_id",
    "Order Number": "order_id",
    "Order No": "order_id",
    "OrderNo": "order_id",
    "Order no": "order_id",

    # Date
    "Order_Date": "order_date",
    "Order Date": "order_date",
    "OrderDate": "order_date",
    "Date": "order_date",
    "Sale Date": "order_date",
    "Transaction Date": "order_date",

    # Customer
    "Customer_ID": "customer_id",
    "Customer Id": "customer_id",
    "CustomerID": "customer_id",
    "Customer code": "customer_id",
    "Customer_code": "customer_id",
    "Customer Code": "customer_id",
    "Customer ID": "customer_id",
    "Customer_id": "customer_id",
    "customer_id": "customer_id",
    "Customer": "customer_id",

    # Product
    "Product_ID": "product_id",
    "Product Id": "product_id",
    "ProductID": "product_id",
    "Product": "product_id",
    "Item_code": "product_id",
    "Product_code": "product_id",
    "Item Code": "product_id",
    "Product Code": "product_id",

    # Region
    "Region": "region",

    # Quantity
    "Quantity": "quantity",
    "Qty": "quantity",
    "Units": "quantity",
    "Qty Sold": "quantity",
    "Units Sold": "quantity",

    # Price
    "Unit_Price": "unit_price",
    "Unit Price": "unit_price",
    "UnitPrice": "unit_price",
    "Price": "unit_price",
    "Unit Cost": "unit_price",
    "Price Per Unit": "unit_price",

    # Discount
    "Discount": "discount",

    # Sales
    "Sales_Amount": "sales_amount",
    "Sales Amount": "sales_amount",
    "SalesAmount": "sales_amount",
    "Total Sales": "sales_amount",
    "Revenue": "sales_amount",
    "Net Sales": "sales_amount"

    
}

# =========================
# LOAD RAW FILES FOR FACT
# =========================

#fact_dataframes = []

sales_data = []

for file in files:
    df = pd.read_excel(RAW_DATA / file)

    print("\nFile: file")
    print("Columns:", df.columns.tolist())
#    fact_dataframes.append(df)

# sales_data = []

#for df in fact_dataframes:

    temp_df = df.copy()

    temp_df.rename(
        columns=sales_columns,
        inplace=True
    )

    if file == "sales_jan.xlsx":
        temp_df["order_date"] = pd.to_datetime(
            temp_df["order_date"],
            format="%Y-%m-%d",
            errors="coerce"
        )

    elif file == "sales_feb.xlsx":
        temp_df["order_date"] = pd.to_datetime(
            temp_df["order_date"],
            format="%d/%m/%Y",
            errors="coerce"
        )

    elif file == "sales_mar.xlsx":
        temp_df["order_date"] = pd.to_datetime(
            temp_df["order_date"],
            format="%d-%b-%Y",
            errors="coerce"
        )

    elif file == "sales_apr.xlsx":
        temp_df["order_date"] = pd.to_datetime(
            temp_df["order_date"],
            format="%m/%d/%Y",
            errors="coerce"
        )

    elif file == "sales_may.xlsx":
        temp_df["order_date"] = pd.to_datetime(
            temp_df["order_date"],
            format="%Y/%m/%d",
            errors="coerce"
        )

    elif file == "sales_june.xlsx":
        temp_df["order_date"] = pd.to_datetime(
            temp_df["order_date"],
            format="%d.%m.%Y",
            errors="coerce"
        )

    elif file == "sales_july.xlsx":
        temp_df["order_date"] = pd.to_datetime(
            temp_df["order_date"],
            format="%d-%m-%Y",
            errors="coerce"
        )

    else:
        temp_df["order_date"] = pd.to_datetime(
            temp_df["order_date"],
            errors="coerce"
        ).dt.date


    print("\nRenamed columns:",list(temp_df.columns))

    print("Missing order dates:", temp_df["order_date"].isna().sum())
    print("Date sample:", temp_df["order_date"].head())

    sales_data.append(
        temp_df[
            [
                "order_id",
                "order_date",
                "customer_id",
                "product_id",
                "region",
                "quantity",
                "unit_price",
                "discount",
                "sales_amount"
            ]
        ]
    )

sales = pd.concat(sales_data,ignore_index=True)

print(
    "Missing order dates:",
    sales["order_date"].isna().sum()
)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

## Convert order_date to datetime
sales["order_date"] = pd.to_datetime(
    sales["order_date"],
    errors="coerce"
)

customer_lookup = pd.read_sql(
    """
    SELECT customer_key, customer_id
    FROM dim_customer
    """,
    conn
)

product_lookup = pd.read_sql(
    """
    SELECT product_key, product_id
    FROM dim_product
    """,
    conn
)

region_lookup = pd.read_sql(
    """
    SELECT region_key, region_name
    FROM dim_region
    """,
    conn
)

date_lookup = pd.read_sql(
    """
    SELECT date_key, full_date
    FROM dim_date
    """,
    conn
)

date_lookup["full_date"] = pd.to_datetime(
    date_lookup["full_date"]
).dt.date

# Merge sales with dimension tables to get foreign keys
sales = sales.merge(
    customer_lookup,
    on="customer_id",
    how="left"
)

sales = sales.merge(
    product_lookup,
    on="product_id",
    how="left"
)

sales = sales.merge(
    region_lookup,
    left_on="region",
    right_on="region_name",
    how="left"
)

invalid_sales = sales[
    sales["order_date"].isna()
    | sales["customer_id"].isna()
    | sales["product_id"].isna()
    | sales["region"].isna()
].copy()

print("\nINVALID FACT ROWS:", len(invalid_sales))

print("\nInvalid rows:")
print(invalid_sales)

sales = sales[
    sales["order_date"].notna()
    & sales["customer_id"].notna()
    & sales["product_id"].notna()
    & sales["region"].notna()
].copy()

print("\nVALID FACT ROWS:", len(sales))

sales["order_date"] = pd.to_datetime(
    sales["order_date"],
    errors="coerce"
).dt.normalize()

date_lookup["full_date"] = pd.to_datetime(
    date_lookup["full_date"]
).dt.normalize()

sales = sales.merge(
    date_lookup,
    left_on="order_date",
    right_on="full_date",
    how="left"
)

print("\nFACT LOOKUP VALIDATION")


print(
    "Missing customer keys:",
    sales["customer_key"].isna().sum()
)

print(
    "Missing product keys:",
    sales["product_key"].isna().sum()
)

print(
    "Missing region keys:",
    sales["region_key"].isna().sum()
)

print(
    "Missing date keys:",
    sales["date_key"].isna().sum()
)


cursor = conn.cursor()

incremental_load = len(sys.argv) > 1



# =========================
# PREPARE FACT DATA
# =========================

# Remove rows where any required dimension key is missing
fact_sales = sales.dropna(
    subset=[
        "date_key",
        "customer_key",
        "product_key",
        "region_key"
    ]
).copy()

print("\nVALID FACT ROWS BEFORE DEDUPLICATION:", len(fact_sales))


# Remove exact duplicate fact records
fact_sales = fact_sales.drop_duplicates(
    subset=[
        "order_id",
        "date_key",
        "customer_key",
        "product_key",
        "region_key",
        "quantity",
        "unit_price",
        "discount",
        "sales_amount"
    ]
).copy()

print("VALID FACT ROWS AFTER DEDUPLICATION:", len(fact_sales))


try:

    if incremental_load:
        print("\nIncremental fact load...")
    else:
        print("\nClearing existing fact_sales...")
        cursor.execute(
            "TRUNCATE TABLE fact_sales RESTART IDENTITY;"
        )

    # =========================
    # LOAD DIMENSION TABLES
    # =========================

    for _, row in customers.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_customer (customer_id, customer_name)
            VALUES (%s, %s)
            ON CONFLICT (customer_id) DO NOTHING
            """,
            (row["customer_id"], row["customer_name"])
        )

    for _, row in products.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_product
            (product_id, product_name, unit_price)
            VALUES (%s, %s, %s)
            ON CONFLICT (product_id) DO NOTHING
            """,
            (
                row["product_id"],
                row["product_name"],
                row["unit_price"]
            )
        )

    for _, row in regions.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_region (region_name)
            VALUES (%s)
            ON CONFLICT (region_name) DO NOTHING
            """,
            (row["region_name"],)
        )

    # =========================
    # LOAD FACT TABLE
    # =========================

    print("\nLoading fact_sales...")

    insert_sql = """
    INSERT INTO fact_sales (
        order_id,
        date_key,
        customer_key,
        product_key,
        region_key,
        quantity,
        unit_price,
        discount,
        sales_amount
    )
    SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s
    WHERE NOT EXISTS (
        SELECT 1
        FROM fact_sales
        WHERE order_id = %s
          AND date_key = %s
          AND customer_key = %s
          AND product_key = %s
          AND region_key = %s
          AND quantity = %s
          AND unit_price = %s
          AND discount = %s
          AND sales_amount = %s
    );
    """

    inserted = 0
    skipped = 0

    for _, row in fact_sales.iterrows():

        values = (
            row["order_id"],
            int(row["date_key"]),
            int(row["customer_key"]),
            int(row["product_key"]),
            int(row["region_key"]),
            int(row["quantity"]),
            float(row["unit_price"]),
            float(row["discount"]),
            float(row["sales_amount"])
        )

        cursor.execute(
            insert_sql,
            values + values
        )

        if cursor.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

    # IMPORTANT: commit AFTER the entire loop
    conn.commit()

    print("\nFACT LOAD COMPLETE")
    print("Rows inserted:", inserted)
    print("Rows skipped:", skipped)

#    if len(fact_sales) > 0 and inserted == 0:
#        raise Exception(
#            "ETL loaded 0 new rows into fact_sales."
#        )

except Exception as e:

    conn.rollback()

    print("\nETL FAILED")
    print("Error:", e)
    print("Database changes rolled back.")

    cursor.close()
    conn.close()

    raise


with open(PROCESSED_FILE, "a") as file:
    for filename in files:
        file.write(filename + "\n")

print("\nPROCESSED FILES UPDATED")

cursor.close()
conn.close()