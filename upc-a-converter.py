from inventree.api import InvenTreeAPI
from inventree.part import Part
import re
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Retrieve server address, username, and password from environment variables
SERVER_ADDRESS = os.environ.get('INVENTREE_SERVER_ADDRESS')
MY_USERNAME = os.environ.get('INVENTREE_USERNAME')
MY_PASSWORD = os.environ.get('INVENTREE_PASSWORD')

# Initialize the InvenTree API client
inventree_api = InvenTreeAPI(
    SERVER_ADDRESS, username=MY_USERNAME, password=MY_PASSWORD, timeout=3600)

# Define the Part ID you want to work with
part_id = 3000

# Retrieve the Part object using InvenTree API
part = Part(inventree_api, part_id)

# Get the UPC-A code from the Part object
upc_a = part.IPN

# Check if the UPC-A code has 11 digits
if len(upc_a) == 11:
    total_sum = 0

    # Calculate the UPC-A checksum
    for i in range(0, 11):
        digit = int(upc_a[i])
        total_sum += digit * (3 if i % 2 == 0 else 1)

    upc_a_checksum = (10 - (total_sum % 10)) % 10

    # Append the checksum to the UPC-A code
    complete_upc_a = upc_a + str(upc_a_checksum)

    # Update the IPN field of the Part object with the new UPC-A code
    part.save(data={"IPN": complete_upc_a})

    # Print the corrected UPC-A code
    print(f"Corrected UPC-A: {complete_upc_a}")

# Check if the UPC-A code has 12 digits
elif len(upc_a) == 12:
    # If the IPN is already 12 digits, validate it and calculate the checksum
    if re.match(r'^\d{12}$', upc_a):
        total_sum = 0

        # Calculate the UPC-A checksum
        for i in range(0, 11):
            digit = int(upc_a[i])
            total_sum += digit * (3 if i % 2 == 0 else 1)

        upc_a_checksum = (10 - (total_sum % 10)) % 10

        # Calculate the complete UPC-A code
        complete_upc_a = upc_a[:11] + str(upc_a_checksum)

        # Update the IPN field of the Part object with the new UPC-A code
        part.save(data={"IPN": complete_upc_a})

        # Print the original and corrected UPC-A codes
        print(f"Original UPC-A: {upc_a} - Corrected UPC-A: {complete_upc_a}")

    else:
        print("The UPC-A code must have exactly 11 or 12 valid digits")

else:
    print("The UPC-A code must have exactly 11 or 12 valid digits")
