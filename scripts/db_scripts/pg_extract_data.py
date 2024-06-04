import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

engine = create_engine(os.getenv('POSTGRESQL_CONN'))

def export_table_to_csv(table_name, csv_file_path):
    """_summary_

    Args:
        table_name (string): Table name to extract data
        csv_file_path (string): Filepath to save extracted data
    """
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    df.to_csv(csv_file_path, index=False)
    print(f"---> Data successfully exported from the table {table_name} a {csv_file_path} ✅")

output_folder = 'data/processed'
os.makedirs(output_folder, exist_ok=True)


export_table_to_csv('public_public.locations_processed', os.path.join(output_folder, 'locations_processed.csv'))
export_table_to_csv('public_public.gentrification_processed', os.path.join(output_folder, 'gentrification_processed.csv'))
