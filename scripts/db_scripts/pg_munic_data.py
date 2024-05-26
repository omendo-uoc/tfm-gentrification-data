import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

file_path = 'data/processed/municipality_master.csv'
df = pd.read_csv(file_path)

engine = create_engine(os.getenv('POSTGRESQL_CONN'))

create_table_query = """
CREATE TABLE IF NOT EXISTS municipality_master (
    id SERIAL PRIMARY KEY,
    munic_cp VARCHAR(10) NOT NULL,
    munic_name VARCHAR(255) NOT NULL
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query))

df.to_sql('municipality_master', engine, if_exists='replace', index=False)

print("\n---> Data successfully loaded in the table municipality_master ✅")