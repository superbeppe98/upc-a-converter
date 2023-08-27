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

# Recupera la lista degli oggetti Part utilizzando InvenTree API
parts = Part.list(inventree_api)

for part in parts:
    ean12 = part.get_field("EAN-12")

    if ean12:
        # Rimuovi eventuali caratteri non numerici dal codice EAN-12
        ean12_digits = re.sub(r'\D', '', ean12)

        # Assicurati che il codice EAN-12 sia esattamente di 12 cifre
        if len(ean12_digits) == 12:
            # Calcola la cifra di controllo per il codice EAN-12
            odd_sum = sum(int(digit) for digit in ean12_digits[-1::-2])
            even_sum = sum(int(digit) for digit in ean12_digits[-2::-2]) * 3
            total_sum = odd_sum + even_sum
            ean12_checksum = (10 - (total_sum % 10)) % 10

            # Aggiungi la cifra di controllo al codice EAN-12 per ottenere il codice EAN-13
            ean13 = ean12_digits + str(ean12_checksum)

            # Aggiorna il campo EAN-12 dell'oggetto Part con il nuovo codice EAN-13
            part.EAN_12 = ean13
            part.save()

            # Stampa il risultato dell'aggiornamento
            print(f"Aggiornato IPN: {part.IPN} - Nuovo EAN-13: {ean13}")
