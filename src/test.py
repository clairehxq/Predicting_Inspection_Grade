import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set(style="ticks", palette="muted", color_codes=True)

def check_folder():
    if os.path.exists('data'):
        pass
    else:
        os.mkdir('data')
      
def check_missing_value(df1, df2, merge):
    print ("There might be some missing match arount {}"
            .format(max(len(df1), len(df2)) - len(merge)))


def preprocessing(query, conn, BBLs):
    '''
    getting buidling data in BBL
    '''
    df = pd.read_sql(query, conn)
    df = df[df['bbl'].isin(BBLs)]
    
    return df

def without_outliers (df, col, thresh=2):
    upper = df[col].mean() + thresh*df[col].std()
    lower = df[col].mean() - thresh*df[col].std()
    df = df[ (df[col] > lower) & (df[col] < upper)]
    return df

def plot_cdf_comparison(df1, df2):
    
    cols = df.select_dtypes(include=['float64']).columns.values

    for col in cols:
        fig, ax = plt.subplots(figsize=(8,6))

        temp_whole = without_outliers(df1, col,2)
        temp_whole[col].hist(normed=1, ax=ax, alpha=0.5, label='universe')
        temp_les = without_outliers(df2, col,2)
        temp_les[col].hist(normed=1, ax=ax, alpha=0.5, label='targeting')
        plt.legend()
        plt.ylabel('Distribution', fontsize=14)
        plt.xlabel('{}'.format(col), fontsize=14)
        plt.savefig('./figs/{}_statistic_normed.png'.format(col))

def plot_pdf_comparison(df1, df2):
    
    cols = df.select_dtypes(include=['float64']).columns.values

    for col in cols:

        fig, ax = plt.subplots(figsize=(8,6))
        df[col].hist(cumulative=True, normed=1, bins=100, ax=ax, alpha=0.5, label='universe')
        les_score[col].hist(cumulative=True, normed=1, bins=100, ax=ax, alpha=0.5, label='targeting')
        plt.legend()
        plt.ylabel('CDF', fontsize=14)
        plt.xlabel('{}'.format(col), fontsize=14)
        plt.savefig('./figs/{}_statistic_CDF.png'.format(col))
    


dataframe = pd.read_csv('C:/Users/Henry Lin/Downloads/'+
                   'cbra_score_new.csv', index_col=0)
df.info()
df = df[df.age!=2017]

df['age'].hist()