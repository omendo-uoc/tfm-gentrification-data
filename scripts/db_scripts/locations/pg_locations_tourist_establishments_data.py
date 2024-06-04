import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()

engine = create_engine(os.getenv('POSTGRESQL_CONN'))

column_definitions = """
actividad_tipo VARCHAR(255),
nombre VARCHAR(255),
tipo_via_codigo VARCHAR(255),
tipo_via_descripcion VARCHAR(255),
direccion_nombre_via VARCHAR(255),
direccion_numero VARCHAR(255),
direccion_codigo_postal FLOAT,
municipio_codigo INT,
municipio_nombre VARCHAR(255),
referencia VARCHAR(255),
web VARCHAR(255),
email VARCHAR(255),
telefono FLOAT,
fax FLOAT,
longitud FLOAT,
latitud FLOAT,
fecha_creacion TIMESTAMP,
fecha_actualizacion TIMESTAMP
"""

# Consulta para crear la tabla si no existe
create_table_query = f"""
CREATE TABLE IF NOT EXISTS locations_tourism_establishments (
    id SERIAL PRIMARY KEY,
    {column_definitions}
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query))

file_path = 'data/raw/locations/tfm_loc_aloj_tur_agen_viaj.csv'
df = pd.read_csv(file_path)

print(df.head())

df.to_sql('locations_tourism_establishments', engine, if_exists='replace', index=False)

print("\n---> Data successfully loaded in the table locations_tourism_establishments ✅")