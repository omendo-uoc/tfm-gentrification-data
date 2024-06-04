import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()

file_path = 'data/raw/tourism/tfm_tur_establ_abier.tsv'
df = pd.read_csv(file_path, sep='\t')

df = df.rename(columns={
    'TERRITORIO': 'munic_name',
    'MEDIDAS': 'measure',
    'ALOJAMIENTO_TURISTICO_CATEGORIA': 'category',
    'OBS_VALUE': 'value',
    'TIME_PERIOD': 'year'
})

print(df.head())

engine = create_engine(os.getenv('POSTGRESQL_CONN'))

create_table_query = """
CREATE TABLE IF NOT EXISTS tourism_establishments (
    id SERIAL PRIMARY KEY,
    munic_name VARCHAR(255) NOT NULL,
    measure VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    value FLOAT NOT NULL,
    year INT NOT NULL
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query))

df.to_sql('tourism_establishments', engine, if_exists='replace', index=False)

print("\n---> Data successfully loaded in the table tourism_establishments ✅")