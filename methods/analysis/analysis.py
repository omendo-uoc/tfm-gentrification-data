import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os


filepath = 'data/processed/gentrification_processed.csv'
df = pd.read_csv(filepath)

df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.year

def plot_variable_by_municipality(df, variable):
    """Method to plot variables of Dataframe by year and municipality

    Args:
        df (DataFrame): Dataframe to analyze
        variable (string): Columns of dataframe

    Returns:
        None: None
    """
    g = sns.FacetGrid(df, col='munic_name', col_wrap=8, height=1.5, aspect=1.2)


    def fill_between_plot(x, y, **kwargs):
        """Method to make a filled area plot

        Args:
            x: X point
            y: Y point

        Returns:
            None: None
        """
        plt.fill_between(x, y, alpha=0.3)
        plt.plot(x, y, alpha=0.6)

    g.map(fill_between_plot, 'year', variable)

    g.set_titles("{col_name}")
    g.set_axis_labels('Año', variable)
    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(90)

    g.fig.suptitle(f'Evolución de {variable} por Municipio', y=1.02)

    plt.show()


def calculate_variations(df, variable, output_path):
    """Method to calculate variable variation by years

    Args:
        df (DataFrame): Dataframe to analyze
        variable (string): Column of Dataframe 
        output_path (string): Output path

    Returns:
        variation_df: New Dataframe
    """
    variation_df = df.groupby('munic_name').agg(
        first_year=pd.NamedAgg(column='year', aggfunc='min'),
        last_year=pd.NamedAgg(column='year', aggfunc='max'),
        first_value=pd.NamedAgg(column=variable, aggfunc='first'),
        last_value=pd.NamedAgg(column=variable, aggfunc='last')
    )
    
    variation_df['variation_%'] = ((variation_df['last_value'] - variation_df['first_value']) / variation_df['first_value']) * 100
    variation_df.to_csv(output_path, index=False)
    return variation_df[['first_year', 'last_year', 'first_value', 'last_value', 'variation_%']]

variables = [
    'population_total', 'births', 'deaths', 'foreigns', 'migrations', 
    'mean_age', 'number_realestate', 'number_hostelry', 'number_entertainment', 
    'number_building', 'sale_price_m2', 'rent_price_m2', 'employment_total', 
    'employment_building', 'employment_commerce', 'employment_hostelry', 
    'employment_services', 'unemployment_total', 'income_per_household', 
    'income_per_person', 'number_crimes', 'open_establishments', 'tourism_spending'
]


output_dir = 'data/final'
os.makedirs(output_dir, exist_ok=True)

for variable in variables:
    print(f'--- {variable} ---')
    plot_variable_by_municipality(df, variable)
    output_path = os.path.join(output_dir, f'{variable}_variation.csv')
    variation_df = calculate_variations(df, variable, output_path)
    print(variation_df)
