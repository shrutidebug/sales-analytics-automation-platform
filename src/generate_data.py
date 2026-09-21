import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker()

#file paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Define regions
regions = [
    "North",
    "South",
    "East",
    "West",
]

#Define products with their unit prices
products = [
    {
        "Product_ID": "P001",
        "Product_Name": "Laptop",
        "Unit_Price": 55000
    },
    {
        "Product_ID": "P002",
        "Product_Name": "Monitor",
        "Unit_Price": 18000
    },
    {
        "Product_ID": "P003",
        "Product_Name": "Keyboard",
        "Unit_Price": 2500
    },
    {
        "Product_ID": "P004",
        "Product_Name": "Mouse",
        "Unit_Price": 1200
    },
    {
        "Product_ID": "P005",
        "Product_Name": "Headphones",
        "Unit_Price": 3500
    }
]

# Generate a list of 500 unique customers with IDs and names.
customers = []

for i in range(1, 501):
    customers.append({
        "Customer_ID": f"CUST{i:04d}",
        "Customer_Name": fake.name()
    })

# Function to generate sales data
def generate_sales_data(start_date, end_date, num_records, order_start):
    records = []

    for i in range(num_records):
        customer = random.choice(customers)
        product = random.choice(products)

        order_date = fake.date_between(
            start_date=start_date,
            end_date=end_date
        )

        quantity = random.randint(1, 10)
        discount = random.choice([0, 0.05, 0.10, 0.15])

        sales_amount = (
            quantity
            * product["Unit_Price"]
            * (1 - discount)
        )

        record = {
            "Order_ID": f"ORD{order_start + i + 1:05d}",
            "Order_Date": order_date,
            "Customer_ID": customer["Customer_ID"],
            "Customer_Name": customer["Customer_Name"],
            "Product_ID": product["Product_ID"],
            "Product_Name": product["Product_Name"],
            "Region": random.choice(regions),
            "Quantity": quantity,
            "Unit_Price": product["Unit_Price"],
            "Discount": discount,
            "Sales_Amount": round(sales_amount, 2)
        }

        records.append(record)

    return pd.DataFrame(records)

# Function to introduce data quality issues
def introduce_data_quality_issues(df):
    df = df.copy()

    #Duplicate order IDs
    duplicate_count = max(1, int(len(df) * 0.01))

    duplicate_rows = df.sample(
        n=duplicate_count,
        random_state=42
    )

    df = pd.concat(
        [df, duplicate_rows],
        ignore_index=True
    )

    #Blank rows

    blank_count = max(1, int(len(df) * 0.005))

    for _ in range(blank_count):
        blank_rows = pd.DataFrame(
            [[None] * len(df.columns)] * blank_count,
            columns=df.columns
    )  
        insert_position = random.randint(0, len(df))

    df = pd.concat(
        [df.iloc[:insert_position], 
         blank_rows, 
         df.iloc[insert_position:]
         ],
        ignore_index=True
    )


    #Missing values in Customer_ID

    missing_customer_count = max(1, int(len(df) * 0.005))

    missing_customer_rows = df.sample(
        n=missing_customer_count,
        random_state=10
    ).index

    df.loc[missing_customer_rows, "Customer_ID"] = None

    #Missing values in Product_ID

    missing_product_count = max(1, int(len(df) * 0.005))

    missing_product_rows = df.sample(
        n=missing_product_count,
        random_state=20
    ).index

    df.loc[missing_product_rows, "Product_ID"] = None

    return df

# Function to apply different column variations based on the month.
def apply_column_variations(df, month):
    df = df.copy()

    if month == "jan":
        # Keep the standard column names
        pass

    elif month == "feb":
        df = df.rename(columns={
            "Order_ID": "Order ID",
            "Order_Date": "Order Date",
            "Customer_ID": "Customer Id",
            "Customer_Name": "Customer Name",
            "Product_ID": "Product Id",
            "Product_Name": "Product Name",
            "Quantity": "Qty",
            "Unit_Price": "Unit Price",
            "Sales_Amount": "Sales Amount"
        })

    elif month == "mar":
        df = df.rename(columns={
            "Order_ID": "OrderID",
            "Order_Date": "OrderDate",
            "Customer_ID": "CustomerID",
            "Product_ID": "ProductID",
            "Unit_Price": "UnitPrice",
            "Sales_Amount": "SalesAmount"
        })

    elif month == "apr":
        df = df.rename(columns={
            "Order_ID": "Order Number",
            "Order_Date": "Date",
            "Customer_ID": "Customer",
            "Product_ID": "Product",
            "Quantity": "Units",
            "Unit_Price": "Price",
            "Sales_Amount": "Total Sales"
        })

    elif month == "may":
        df = df.rename(columns={
            "Order_ID": "Order No",
            "Order_Date": "Sale Date",
            "Customer_ID": "Customer Code",
            "Customer_Name": "Customer_name",
            "Product_ID": "Item Code",
            "Product_Name": "Item Name",
            "Quantity": "Qty Sold",
            "Unit_Price": "Price Per Unit",
            "Sales_Amount": "Revenue"
    })

    elif month == "june":
        df = df.rename(columns={
            "Order_ID": "Order Number",
            "Order_Date": "Transaction Date",
            "Customer_ID": "Customer ID",
            "Product_ID": "Product Code",
            "Quantity": "Units Sold",
            "Unit_Price": "Unit Cost",
            "Sales_Amount": "Net Sales"
    })


    return df

# Function to apply different date formats based on the month.
def apply_date_format(df, month):
    df = df.copy()

    if month == "jan":
        df["Order_Date"] = df["Order_Date"].apply(
            lambda x: x.strftime("%Y-%m-%d")
            if pd.notna(x) else x
        )

    elif month == "feb":
        df["Order Date"] = df["Order Date"].apply(
            lambda x: x.strftime("%d/%m/%Y")
            if pd.notna(x) else x
        )

    elif month == "mar":
        df["OrderDate"] = df["OrderDate"].apply(
            lambda x: x.strftime("%d-%b-%Y")
            if pd.notna(x) else x
        )

    elif month == "apr":
        df["Date"] = df["Date"].apply(
            lambda x: x.strftime("%m/%d/%Y")
            if pd.notna(x) else x
        )

    elif month == "may":
        df["Sale Date"] = df["Sale Date"].apply(
            lambda x: x.strftime("%Y/%m/%d")
            if pd.notna(x) else x
        )

    elif month == "june":
        df["Transaction Date"] = df["Transaction Date"].apply(
            lambda x: x.strftime("%d.%m.%Y")
            if pd.notna(x) else x
        )

    return df

# Function to generate monthly sales data files with variations and issues.
def generate_monthly_file(
    start_date,
    end_date,
    num_records,
    file_name,
    month,
    order_start
):
    df = generate_sales_data(
        start_date=start_date,
        end_date=end_date,
        num_records=num_records,
        order_start=order_start
    )

    df = introduce_data_quality_issues(df)

    df = apply_column_variations(df, month)

    df = apply_date_format(df, month)

    output_path = RAW_DATA_DIR / file_name

    df.to_excel(
        output_path,
        index=False
    )

    print(f"Created: {output_path}")
    print(f"Rows: {len(df)}")
    print("-" * 50)

#Generate January file
generate_monthly_file(
   start_date=datetime(2026, 1, 1),
    end_date=datetime(2026, 1, 31),
    num_records=1250,
    file_name="sales_jan.xlsx",
    month="jan",
    order_start=1
)

#Generate February file
generate_monthly_file(
    start_date=datetime(2026, 2, 1),
    end_date=datetime(2026, 2, 28),
    num_records=1250,
    file_name="sales_feb.xlsx",
    month="feb",
    order_start=1251
)

#Generate March file
generate_monthly_file(
    start_date=datetime(2026, 3, 1),
    end_date=datetime(2026, 3, 31),
    num_records=1250,
    file_name="sales_mar.xlsx",
    month="mar",
    order_start=2501
)


#Generate April file
generate_monthly_file(
    start_date=datetime(2026, 4, 1),
    end_date=datetime(2026, 4, 30),
    num_records=1250,
    file_name="sales_apr.xlsx",
    month="apr",
    order_start=3751
)


# Generate May file
generate_monthly_file(
    start_date=datetime(2026, 5, 1),
    end_date=datetime(2026, 5, 31),
    num_records=1250,
    file_name="sales_may.xlsx",
    month="may",
    order_start=5001
)

# Generate June file
generate_monthly_file(
    start_date=datetime(2026, 6, 1),
    end_date=datetime(2026, 6, 30),
    num_records=1250,
    file_name="sales_june.xlsx",
    month="june",
    order_start=6251
)

#Generate July file
generate_monthly_file(
    start_date=datetime(2026, 7, 1),
    end_date=datetime(2026, 7, 31),
    num_records=1250,
    file_name="sales_july.xlsx",
    month="july",
    order_start=7501
)

#Generate August file
generate_monthly_file(
    start_date=datetime(2026, 8, 1),
    end_date=datetime(2026, 8, 31),
    num_records=1250,
    file_name="sales_aug.xlsx",
    month="august",
    order_start=8751
)

#Generate September file
generate_monthly_file(
    start_date=datetime(2026, 9, 1),
    end_date=datetime(2026, 9, 30),
    num_records=1250,
    file_name="sales_sept.xlsx",
    month="september",
    order_start=10001
)

#Generate October file
generate_monthly_file(
    start_date=datetime(2026, 10, 1),
    end_date=datetime(2026, 10, 31),
    num_records=1250,
    file_name="sales_oct.xlsx",
    month="october",
    order_start=11251
)

#Generate November file
generate_monthly_file(
    start_date=datetime(2026, 11, 1),
    end_date=datetime(2026, 11, 30),
    num_records=1250,
    file_name="sales_nov.xlsx",
    month="november",
    order_start=12501
)

#Generate December file
generate_monthly_file(
    start_date=datetime(2026, 12, 1),
    end_date=datetime(2026, 12, 31),
    num_records=1250,
    file_name="sales_dec.xlsx",
    month="december",
    order_start=13751
)