from inventree.api import InvenTreeAPI
from inventree.part import Part
import re
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_ADDRESS = os.environ.get('INVENTREE_SERVER_ADDRESS')
MY_USERNAME = os.environ.get('INVENTREE_USERNAME')
MY_PASSWORD = os.environ.get('INVENTREE_PASSWORD')
inventree_api = InvenTreeAPI(SERVER_ADDRESS, username=MY_USERNAME,
                             password=MY_PASSWORD, timeout=3600)

# Retrieve the list of Part objects using InvenTree API
parts = Part.list(inventree_api)

# Sort the Part objects based on the new UPC-A code
sorted_parts = sorted(parts, key=lambda part: part.IPN)

for index, part in enumerate(sorted_parts, start=1):
    upc_a = part.IPN  # Change variable name to upc_a

    # Ensure that the UPC-A code is exactly 11 digits
    if len(upc_a) == 11:  # Change comment to UPC-A
        # Calculate the checksum for the UPC-A code (last digit)
        total_sum = 0

        for i in range(0, 11):
            digit = int(upc_a[i])
            total_sum += digit * (3 if i % 2 == 0 else 1)

        upc_a_checksum = (10 - (total_sum % 10)) % 10

        # Add the checksum to the UPC-A code to get the complete UPC-A code
        complete_upc_a = upc_a + str(upc_a_checksum)

        # Update the IPN field of the Part object with the new UPC-A code
        part.save(data={"IPN": complete_upc_a})

        # Print the complete UPC-A code
        print(f"Complete UPC-A: {complete_upc_a}")  # Change comment to UPC-A

    elif len(upc_a) == 12 and re.match(r'^\d{11}$', upc_a[:11]):
        # If the IPN is already a valid UPC-A code (11 digits) and ends with '0',
        # keep it unchanged and print it
        complete_upc_a = upc_a  # Change comment to UPC-A
        # Change comment to UPC-A
        print(f"UPC-A: {upc_a} - Unchanged UPC-A: {complete_upc_a}")

    elif len(upc_a) == 12:
        # Take the first 11 digits of the UPC-A code
        upc_a = upc_a[:11]  # Change variable name to upc_a

        # Calculate the checksum for the UPC-A code (last digit)
        total_sum = 0

        for i in range(0, 11):
            digit = int(upc_a[i])
            total_sum += digit * (3 if i % 2 == 0 else 1)

        upc_a_checksum = (10 - (total_sum % 10)) % 10

        # Add the checksum to the UPC-A code to get the complete UPC-A code
        complete_upc_a = upc_a + str(upc_a_checksum)

        # Update the IPN field of the Part object with the new UPC-A code
        part.save(data={"IPN": complete_upc_a})

        # Print the complete UPC-A code for each UPC-A input
        # Change comment to UPC-A
        print(f"UPC-A: {upc_a} - Complete UPC-A: {complete_upc_a}")
