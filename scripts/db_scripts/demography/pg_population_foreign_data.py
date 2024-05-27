import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()

file_path = 'data/raw/demography/tfm_demo_pob_extr.tsv'
df = pd.read_csv(file_path, sep='\t')

df = df.rename(columns={
    'GEOGRAPHICAL': 'munic_name',
    'MEASURE': 'measure',
    'OBS_VALUE': 'value',
    'TIME': 'year'
})

print(df.head())

engine = create_engine(os.getenv('POSTGRESQL_CONN'))

create_table_query = """
CREATE TABLE IF NOT EXISTS population_foreign (
    id SERIAL PRIMARY KEY,
    munic_name VARCHAR(255) NOT NULL,
    measure VARCHAR(255) NOT NULL,
    value FLOAT NOT NULL,
    year INT NOT NULL
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query))

df.to_sql('population_foreign', engine, if_exists='replace', index=False)

print("\n---> Data successfully loaded in the table population_foreign ✅")