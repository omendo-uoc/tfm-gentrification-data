import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


file_path = 'data/processed/gentrification_processed.csv'
df = pd.read_csv(file_path)

columns = [
    'population_total', 'births', 'deaths', 'foreigns', 'migrations', 
    'mean_age', 'number_realestate', 'number_hostelry', 'number_entertainment', 
    'number_building', 'sale_price_m2', 'rent_price_m2', 'employment_total', 
    'employment_building', 'employment_commerce', 'employment_hostelry', 
    'employment_services', 'unemployment_total', 'income_per_household', 
    'income_per_person', 'number_crimes', 'open_establishments', 'tourism_spending'
]

df_filtered = df[columns]

scaler = StandardScaler()
df_normalized = scaler.fit_transform(df_filtered)

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(df_normalized)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('Método del Codo')
plt.xlabel('Número de Clusters')
plt.ylabel('WCSS')
plt.show()

kmeans = KMeans(n_clusters=3, random_state=0)
df['cluster'] = kmeans.fit_predict(df_normalized)

plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='munic_name', y='year', hue='cluster', palette='viridis')
plt.title('Clusters de Gentrificación por Municipio y Año')
plt.xticks(rotation=90)
plt.show()

df.to_csv('data/processed/gentrification_clusters.csv', index=False)
