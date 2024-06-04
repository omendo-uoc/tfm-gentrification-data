import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()

file_path = 'data/raw/housing/tfm_hou_compra_alq.csv'
df = pd.read_csv(file_path, sep=";")

df = df.rename(columns={
    'MUNICIPIO': 'munic_name',
    'PRECIO_VENTA_M2': 'sale_price_m2',
    'PRECIO_ALQUILER_M2': 'rent_price_m2',
    'ANYO': 'year'
})

print(df.head())

engine = create_engine(os.getenv('POSTGRESQL_CONN'))

create_table_query = """
CREATE TABLE IF NOT EXISTS housing_prices (
    id SERIAL PRIMARY KEY,
    munic_name VARCHAR(255) NOT NULL,
    sale_price_m2 FLOAT NOT NULL,
    rent_price_m2 FLOAT NOT NULL,
    year INT NOT NULL
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query))

df.to_sql('housing_prices', engine, if_exists='replace', index=False)

print("\n---> Data successfully loaded in the table housing_prices ✅")