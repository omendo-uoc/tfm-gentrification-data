import geopandas as gpd
import pandas as pd


geojson_path = 'data/raw/territory/municipios_desde2007_20170101.json'
municipios_gdf = gpd.read_file(geojson_path)

csv_path = 'data/processed/gentrification_4clusters.csv'
gentrification_df = pd.read_csv(csv_path)

municipios_gdf['geocode'] = municipios_gdf['geocode'].astype(str)
gentrification_df['munic_cp'] = gentrification_df['munic_cp'].astype(str)

gentrification_df['year'] = gentrification_df['year'].astype(str).str[:4]
gentrification_df['year'] = pd.to_datetime(gentrification_df['year'], format='%Y')

merged_gdf = municipios_gdf.merge(gentrification_df, left_on='geocode', right_on='munic_cp')

output_geojson_path = 'data/final/merged_gentrification_data_4cluster.geojson'
merged_gdf.to_file(output_geojson_path, driver='GeoJSON')

print(f'---> Merged data saved: {output_geojson_path} ✅')