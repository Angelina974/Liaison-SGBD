from faker import Faker
import psycopg2

fake = Faker()

conn = psycopg2.connect(
    dbname="mydatabase",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

for _ in range(100):
    name = fake.name()
    description = fake.text()
    price = round(fake.random_number(digits=5) / 100, 2)
    cursor.execute(
        "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)",
        (name, description, price)
    )

conn.commit()
cursor.close()
conn.close()
