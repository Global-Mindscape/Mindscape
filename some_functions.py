# function to query the data easily
def query_data(df, code=None, year=None, disease=None):
    mask = df.copy()
    
    if code:
        mask = mask[mask['code'] == code]
    if year:
        mask = mask[mask['year'] == year]
    if disease:
        mask = mask[['code', 'year', disease]]
    else:
        mask = mask[['code', 'year'] + [col for col in mask.columns if col not in ['code', 'year']]]
    
    return mask

# easy correlation for dataframes with object types
def get_corr(df):
    df_copy = df.copy()
    corr_df = df_copy.select_dtypes(include=['float64', 'int64']).corr()
    return corr_df

# plotting correlation heatmap
import matplotlib.pyplot as plt
import seaborn as sns
def print_corr(df):
    plt.figure(figsize=(6, 6))
    sns.heatmap(df, annot=True, cmap='coolwarm', fmt=".2f", square=True)
    plt.title('Correlation Heatmap')
    plt.show()