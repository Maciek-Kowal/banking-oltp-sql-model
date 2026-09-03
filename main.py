from faker import Faker
import random
import os
from dotenv import load_dotenv
import pyodbc
from pyodbc import connect
import sys

fakers = {
    'United Kingdom': Faker('en_GB'),
    'Germany': Faker('de_DE'),
    'Poland': Faker('pl_PL')
}

dane_do_bazy = []
liczba_rekordow = 1000

print("Generowanie danych klientów...")

for _ in range(liczba_rekordow):
    kraj = random.choice(list(fakers.keys()))
    instancja = fakers[kraj]

    # Losujemy 80% detalicznych, 20% firmowych
    typ_klienta = random.choices(['retail', 'corporate'], weights=[0.8, 0.2])[0]

    city = instancja.city()
    state = getattr(instancja, 'administrative_unit', lambda: city)()

    phone = instancja.phone_number()[:15]
    email = instancja.email() if typ_klienta == 'retail' else instancja.company_email()
    postal = instancja.postcode()[:6]
    street = instancja.street_name()
    house_num = instancja.building_number()[:10]
    apt_num = instancja.building_number()[:10] if random.random() > 0.5 else None

    if typ_klienta == 'retail':
        rekord = (
            None,  # parent_company_id
            'retail',  # customer_type
            instancja.first_name(),  # first_name
            None,  # middle_name
            instancja.last_name(),  # last_name
            instancja.bothify('??#########'),  # national_id (max 11 znaków)
            instancja.date_of_birth(minimum_age=18, maximum_age=90),  # birth_date
            None,  # company_name
            None,  # tax_id
            kraj,  # country
            state,  # state_province
            city,  # county
            city,  # municipality
            city,  # city
            postal,  # postal_code
            street,  # street
            house_num,  # house_number
            apt_num,  # apartment_number
            phone,  # phone_number
            email  # email
        )
    else:
        rekord = (
            None,  # parent_company_id
            'corporate',  # customer_type
            None,  # first_name
            None,  # middle_name
            None,  # last_name
            None,  # national_id
            None,  # birth_date
            instancja.company(),  # company_name
            instancja.bothify('##########'),  # tax_id (max 10 znaków)
            kraj,  # country
            state,  # state_province
            city,  # county
            city,  # municipality
            city,  # city
            postal,  # postal_code
            street,  # street
            house_num,  # house_number
            None,  # apartment_number (firmy zazwyczaj bez)
            phone,  # phone_number
            email  # email
        )

    dane_do_bazy.append(rekord)

print(f"Wygenerowano {len(dane_do_bazy)} rekordów.")

load_dotenv()
sterownik = os.getenv('DB_DRIVER')
serwer = os.getenv('DB_SERVER')
baza = os.getenv('DB_DATABASE')
login = os.getenv('DB_USER')
haslo = os.getenv('DB_PASSWORD')

polaczenie = (f"DRIVER={sterownik};"
              f"SERVER={serwer};"
              f"DATABASE={baza};"
              f"uid={login};"
              f"pwd={haslo}"
              )

try:
    connection = pyodbc.connect(polaczenie)
    print("dziala")
except Exception as ex:
    print (f'blad! {ex}')
    sys.exit(1)

