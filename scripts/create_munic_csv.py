import pandas as pd


def get_cp(filepath):
    """Function to get CSV file with municipallity cp and name

    Args:
        filepath (string): Filepath to extract municipallity cp and name
    """
    
    file_path = '../data/raw/locations/tfm_loc_host_rest.csv'

    df = pd.read_csv(file_path)

    df_unique = df[['municipio_codigo', 'municipio_nombre']].drop_duplicates()

    df_unique_sorted = df_unique.rename(columns={'municipio_codigo': 'munic_cp', 'municipio_nombre': 'munic_name'})
    df_unique_sorted = df_unique_sorted.sort_values(by='munic_name', ascending=True)

    print(df_unique_sorted.head())

    output_path = '../data/processed/municipios_tenerife_sorted.csv'
    df_unique_sorted.to_csv(output_path, index=False)

    print(f"\nFile processed and saved as {output_path}")
    

get_cp('../data/raw/locations/tfm_loc_host_rest.csv')