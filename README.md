# UPC-A Code Generation and Part Update Script

This script retrieves a list of Part objects from InvenTree using its API, generates UPC-A codes based on their EAN-11 codes, and updates the Part objects with the new UPC-A codes. The script is written in Python and utilizes the InvenTree API library.

## Installation

The script requires two external dependencies, `inventree` and `python-dotenv`, which can be installed by running the following command in your terminal or command prompt:

```shell
pip install -r requirements.txt
```

## Usage

Run the upc_a_generator.py script:

```shell
python3 upc_a_generator.py
```

The script will establish a connection to your InvenTree server, authenticate using your provided credentials, and retrieve part data. It then proceeds to sort the parts based on their IPN (International Part Number) and generates and assigns UPC-A codes to each Part object.

Upon completion, the script saves the updated Part objects with the new UPC-A codes.

You can review the generated UPC-A codes in the InvenTree database for each respective Part.

Please ensure that you have the necessary access permissions for your InvenTree server and adhere to the server's usage policies.

Note: The script assumes that the Part class has been correctly imported from the inventree module and that the IPN field exists for each Part object in the InvenTree server's data.

Feel free to customize the script to meet your specific requirements and seamlessly integrate it into your InvenTree workflow.

For any inquiries or issues related to the script, consult the script's documentation or reach out to the script's author.

This README provides comprehensive instructions for installing and utilizing your UPC-A code generation and part update script.