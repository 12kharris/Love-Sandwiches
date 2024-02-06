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

    print("Data received")
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


data = get_sales_data()