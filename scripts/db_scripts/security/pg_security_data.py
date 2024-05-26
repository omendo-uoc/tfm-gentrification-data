import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()

engine = create_engine(os.getenv('POSTGRESQL_CONN'))

create_table_query = """
CREATE TABLE IF NOT EXISTS security (
    id SERIAL PRIMARY KEY,
    munic_name VARCHAR(255) NOT NULL,
    value FLOAT NOT NULL,
    year INT NOT NULL
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query))

for year in range(2017, 2024):
    file_path = f'data/raw/security/tfm_ser_crim_{year}.csv'
    df = pd.read_csv(file_path, sep=';', encoding='utf8')
    
    df = df.rename(columns={
        'MUNICIPIO': 'munic_name',
        'VALOR': 'value',
        'ANYO': 'year'
    })
    
    print(df.head())
    
    df.to_sql('security', engine, if_exists='append', index=False)

    print(f"\n---> Data for year {year} successfully loaded in the table security_data ✅")