import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo categorizado
data = pd.read_csv('data/final/locations_categorized.csv')

# Calcular el número de localizaciones por tipo de actividad por municipio
activity_by_municipality = data.groupby(['municipio_nombre', 'nueva_actividad']).size().reset_index(name='count')

# Calcular la media de localizaciones por tipo de actividad en toda la isla
activity_mean = activity_by_municipality.groupby('nueva_actividad')['count'].mean().reset_index(name='mean_count')

# Fusionar la media con los datos originales
merged_data = activity_by_municipality.merge(activity_mean, on='nueva_actividad')

# Crear la visualización
plt.figure(figsize=(14, 8))
sns.barplot(data=merged_data, x='nueva_actividad', y='count', hue='municipio_nombre', dodge=True, palette='Set2')
plt.plot(merged_data['nueva_actividad'], merged_data['mean_count'], color='red', marker='o', linestyle='-', linewidth=2, label='Media de la Isla')
plt.xticks(rotation=90)
plt.xlabel('Tipo de Actividad')
plt.ylabel('Número de Localizaciones')
plt.title('Comparación del Número de Localizaciones por Tipo de Actividad por Municipio en comparación con la Media de la Isla')
plt.legend(title='Municipio')
plt.tight_layout()
plt.show()