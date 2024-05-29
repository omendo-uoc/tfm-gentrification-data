import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


filepath = 'data/processed/gentrification_3clusters.csv'
df = pd.read_csv(filepath)

df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.year
colors = ['#FFD333', '#44AFA0', '#027089']


def calculate_mean_per_year(df, variable):
    return df.groupby(['cluster', 'year'])[variable].mean().reset_index()


def plot_variable_by_cluster(df, variable):
    mean_df = calculate_mean_per_year(df, variable)
    g = sns.FacetGrid(mean_df, col='cluster', col_wrap=3, height=4, aspect=1.5)


    def fill_between_plot(x, y, color, **kwargs):
        plt.fill_between(x, y, color=color, alpha=0.3)
        plt.plot(x, y, color=color, alpha=0.6)

    for idx, ax in enumerate(g.axes.flat):
        cluster = idx
        color = colors[cluster]
        cluster_data = mean_df[mean_df['cluster'] == cluster]
        ax.fill_between(cluster_data['year'], cluster_data[variable], color=color, alpha=0.3)
        ax.plot(cluster_data['year'], cluster_data[variable], color=color, alpha=0.6)

    g.set_titles("Cluster {col_name}")
    g.set_axis_labels('Año', variable)
    for ax in g.axes.flat:
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        for label in ax.get_xticklabels():
            label.set_rotation(90)


    plt.subplots_adjust(top=0.9, bottom=0.15, left=0.1, right=0.95, hspace=0.4, wspace=0.4)
    g.fig.suptitle(f'Evolución de {variable} por Cluster', y=1.02)
    plt.show()

variables = [
    'population_total', 'births', 'deaths', 'foreigns', 'migrations', 
    'mean_age', 'number_realestate', 'number_hostelry', 'number_entertainment', 
    'number_building', 'sale_price_m2', 'rent_price_m2', 'employment_total', 
    'employment_building', 'employment_commerce', 'employment_hostelry', 
    'employment_services', 'unemployment_total', 'income_per_household', 
    'income_per_person', 'number_crimes', 'open_establishments', 'tourism_spending'
]

for variable in variables:
    plot_variable_by_cluster(df, variable)
