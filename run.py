import gspread as gsp
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gsp.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():
    """
    Get sales figures from user input
    """
    print("Please enter sales data from the last market")
    print("Data should be 6 numbers seperated by commas")
    print("Example: 10,20,30,40,50,60\n")

    validated = False

    while(not validated):
        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        validated = validate_data(sales_data)

    print("Data received\n")
    return sales_data


def validate_data(values):
    """
    Validates whether the input data contains the correct number 
    of values and data types
    """
    try:
        if(len(values) != 6):
            raise ValueError(
                f"Invalid data. Expected 6 values, received {len(values)}"
            )
        [int(value) for value in values] #convert each data entry into an int
    except ValueError as e:
        print(e)
        print("Please try again\n")
        return False

    return True

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate  stock surplus for given day
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1] #get last row
    surplus_data = []

    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def update_worksheet(data, sheet_name):
    """
    Update the specified worksheet, add new row with the list data provided
    """
    print(f"Updating {sheet_name} worksheet...\n")
    worksheet = SHEET.worksheet(sheet_name)
    worksheet.append_row(data)
    print(f"{sheet_name} worksheet updated successfully\n")

def get_last_5_sales_entries():
    """
    collects last 5 entries in the sales worksheet
    """
    sales = SHEET.worksheet("sales")
    columns = []

    for i in range(1,7):
        column = sales.col_values(i)
        columns.append(column[-5:]) # get last 5 values

    return columns

def calculate_stock_data(sales):
    """
    calculate the average stock for each item type
    """
    print("Calculating new stock recommendations...\n")
    new_stock_data = []

    for column in sales:
        int_column = [int(num) for num in column] # convert data to ints
        avg = sum(int_column) / len(int_column)
        new_stock = round(avg * 1.1) # add 10% onto the reccommendation
        new_stock_data.append(new_stock)

    return new_stock_data



def main():
    """
    Run the program
    """
    data = get_sales_data()
    sales_data = [int(value) for value in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_sales_entries()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


main()
