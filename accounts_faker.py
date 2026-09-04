import os
import random
from dotenv import load_dotenv
import pyodbc
import sys
from faker import Faker

fake = Faker()
load_dotenv()
polaczenie = (f"DRIVER={os.getenv('DB_DRIVER')};"
              f"SERVER={os.getenv('DB_SERVER')};"
              f"DATABASE={os.getenv('DB_DATABASE')};"
              f"uid={os.getenv('DB_USER')};"
              f"pwd={os.getenv('DB_PASSWORD')}")

try:
    connection = pyodbc.connect(polaczenie)
    cursor = connection.cursor()

    print("Pobieranie ID klientów z bazy")
    cursor.execute("SELECT customer_id FROM customers;")
    klienci = cursor.fetchall()

    dane_kont = []

    print("Generowanie kont bankowych")
    for klient in klienci:
        customer_id = klient[0]

        liczba_kont = random.randint(1, 3)

        for _ in range(liczba_kont):
            account_type = random.choice(['CHECKING', 'SAVINGS', 'CREDIT'])
            iban = fake.iban()
            balance = round(random.uniform(0.0, 50000.0), 2)
            currency = random.choice(['PLN', 'EUR', 'USD', 'GBP'])
            status = random.choices(['ACTIVE', 'BLOCKED', 'CLOSED'], weights=[0.9, 0.05, 0.05])[0]

            rekord = (
                customer_id,  # fk_customer_id
                account_type,  # account_type
                iban,  # IBAN
                balance,  # balance
                currency,  # currency
                status  # status
            )
            dane_kont.append(rekord)
    cursor.fast_executemany = True
    sql_insert_accounts = """
        INSERT INTO accounts (
            customer_id, account_type, IBAN, balance, currency, status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """

    print(f"Wysyłanie {len(dane_kont)} kont do bazy")
    cursor.executemany(sql_insert_accounts, dane_kont)
    connection.commit()
    print("Konta załadowane pomyślnie")

except Exception as ex:
    print(f'Błąd!: {ex}')
    sys.exit(1)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()