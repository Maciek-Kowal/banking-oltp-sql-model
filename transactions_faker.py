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
    print("Pobieranie bazy kont")
    cursor.execute("SELECT account_id, IBAN FROM accounts;")
    konta = cursor.fetchall()

    dane_transakcji = []
    liczba_transakcji = 10000

    print("Generowanie paczki transakcji")
    for _ in range(liczba_transakcji):
        tx_type = random.choice(['INTERNAL', 'EXTERNAL_IN', 'EXTERNAL_OUT'])

        if tx_type == 'INTERNAL':
            sender = random.choice(konta)
            receiver = random.choice(konta)
            while sender[0] == receiver[0]:
                receiver = random.choice(konta)
            s_id, s_iban = sender[0], sender[1]
            r_id, r_iban = receiver[0], receiver[1]

        elif tx_type == 'EXTERNAL_IN':
            receiver = random.choice(konta)
            s_id, s_iban = None, fake.iban()  # Zewnętrzny nadawca
            r_id, r_iban = receiver[0], receiver[1]

        else:
            sender = random.choice(konta)
            s_id, s_iban = sender[0], sender[1]
            r_id, r_iban = None, fake.iban()  # Zewnętrzny odbiorca

        amount = round(random.uniform(5.0, 15000.0), 2)
        status = random.choices(
            ['PENDING', 'COMPLETED', 'FAILED', 'REJECTED', 'CANCELLED'],
            weights=[0.05, 0.85, 0.05, 0.025, 0.025]
        )[0]

        rekord = (s_id, s_iban, r_id, r_iban, amount, status, tx_type)
        dane_transakcji.append(rekord)

    cursor.fast_executemany = True
    sql_insert_tx = """
        INSERT INTO transactions (
            sender_account_id, sender_iban, receiver_account_id, 
            receiver_iban, amount, status, transaction_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    print(f"Wysyłanie {len(dane_transakcji)} transakcji do bazy")
    cursor.executemany(sql_insert_tx, dane_transakcji)
    connection.commit()
    print("Transakcje załadowane pomyślnie")

except Exception as ex:
    print(f'Błąd!: {ex}')
    sys.exit(1)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()