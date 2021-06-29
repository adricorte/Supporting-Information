import pandas as pd
import numpy as np
import sys
from IPython.display import display, HTML
import matplotlib.pyplot as plt
%matplotlib inline
from bokeh.io import export_png, export_svgs
from bokeh.models import ColumnDataSource, DataTable, TableColumn
import os
import dataframe_image as dfi

def save_df_as_image(df, path):
    source = ColumnDataSource(df)
    df_columns = [df.index.name]
    df_columns.extend(df.columns.values)
    columns_for_table=[]
    for column in df_columns:
        columns_for_table.append(TableColumn(field=column, title=column))

    data_table = DataTable(source=source, columns=columns_for_table,height_policy="auto",width_policy="auto",index_position=None)
    export_png(data_table, filename = path)

datasets=['ccsbase','ccscompendium', 'cembio']
tools=['ccsbase', 'deepccs', 'allccs', 'darkchem']
classes=['Glycerolipids','Glycerophospholipids','Sphingolipids','Steroids','Nucleoside_nucleotide','Fatty_acids','Acyl_carnitines','Monosaccharides','Carboxylic_acids','Benzene']

data= pd.DataFrame(columns=['Dataset','Tool', 'Classification', 'Mean_abs','SD_abs','MPE','SD_PE','Outliers','Count'])


for dataset in datasets:
    for tool in tools:

        joined=pd.read_csv('./{}/{}/joined{}.csv'.format(dataset, tool, tool), sep=';')

        for clas in classes:

            classified=joined.loc[joined[clas] == True]

            df10=classified[(classified.percentage_difference>=10) | (classified.percentage_difference<=-10)]

            mean_error= np.mean(np.abs(classified.difference))
            desv_error= np.std(np.abs(classified.difference))

            mean_percentage_error= np.mean(np.abs(classified.percentage_difference))
            desv_percentage_error= np.std(np.abs(classified.percentage_difference))

            d = {'Dataset': [dataset],'Tool': [tool], 'Classification': [clas], 'Mean_abs': [mean_error], 'SD_abs': [desv_error], 'MPE': [mean_percentage_error], 'SD_PE': [desv_percentage_error], 'Outliers': [df10.shape[0]], 'Count': [classified.shape[0]]}
            df = pd.DataFrame(data=d)
            data = pd.concat([data, df])
        


for clas in classes:
    
    if not os.path.exists('tables_classification'):
        os.makedirs('tables_classification')
        
    classify=data.loc[data['Classification'] == clas]
    classify = classify[['Dataset','Tool','MPE','SD_PE','Outliers','Count']]
    classify=classify.sort_values(by='Tool')
    dfi.export(classify, './tables_classification/{}.png'.format(clas))


data= pd.DataFrame(columns=['Dataset','Tool', 'Classification','Mean_perc','SD_perc','Outliers','Count'])



for dataset in datasets:
    for tool in tools:

        joined=pd.read_csv('./{}/{}/joined{}.csv'.format(dataset, tool, tool), sep=';')
        joined.dropna(subset = ['M/Z', 'Predicted CCS', 'CCS'], inplace=True)
      
        for clas in classes:

            classified=joined.loc[joined[clas] == True]

            fig = plt.figure(figsize=(16, 9))
            plt.rcParams['font.size'] = '18' 
            fig.suptitle('{}, data set: {}, tool: {}'.format(clas.upper(), dataset.upper(), tool.upper()), fontsize=22)
            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)
            ax1.scatter(classified['M/Z'],classified['Predicted CCS'], s=2.5,label='Experimental')
            
            if classified.shape[0] > 1:
                b1, m1 = polyfit(classified['M/Z'], classified['Predicted CCS'], 1)
                ax1.plot(classified['M/Z'], b1 + m1 * classified['M/Z'], '-')
        
            ax1.scatter(classified['M/Z'],classified['CCS'], s=2.5,label='Predicted')
            ax1.set_xlabel('M/Z', fontsize=18)
            ax1.set_ylabel('CCS', fontsize=18)
       
            ax1.set_title('M/Z vs. Experimental CCS and Predicted CCS', size=18)
            
            if classified.shape[0]>1:
                b2, m2 = polyfit(classified['M/Z'], classified['CCS'], 1)
                ax1.plot(classified['M/Z'], b2 + m2 * classified['M/Z'], '-')
            
            ax1.legend()
            
            ax2.scatter(classified['CCS'],classified['Predicted CCS'], s=2.5)
            
            if classified.shape[0]>1:
                b3, m3 = polyfit(classified['CCS'], classified['Predicted CCS'], 1)
                ax2.plot(classified['CCS'], b3 + m3 * classified['CCS'], '-')
        
            ax2.set_title('Experimental CCS vs. Predicted CCS', size=18)
            ax2.set_xlabel('Experimental CCS', fontsize=18)
            ax2.set_ylabel('Predicted CCS', fontsize=18)
            ax2.set_xlim([100, 400])
            ax2.set_ylim([100, 400])
            
            fig.savefig('./Figures/Figure_{}_{}_{}.png'.format(dataset, tool, clas), facecolor='w')
            
            plt.show()
            plt.clf()

colors=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:cyan', 'tab:pink']


for dataset in datasets:

    for tool in tools:

        fig = plt.figure(figsize=(16, 9))
        plt.rcParams['font.size'] = '18'

        fig.suptitle('Classifications for predicted CCS values of tool {} with the {} data set'.format(tool.upper(), dataset.upper()), fontsize=22)
        ax1 = fig.add_subplot(111)

        joined=pd.read_csv('./{}/{}/joined{}.csv'.format(dataset, tool, tool), sep=';')
        joined.dropna(subset = ['M/Z', 'Predicted CCS'], inplace=True)

        for clas, color in zip(classes, colors):
            classified=joined.loc[joined[clas] == True]

            ax1.scatter(classified['M/Z'],classified['Predicted CCS'], s=20,label='{}'.format(clas), color=color)
            ax1.set_xlabel('M/Z', fontsize=18)
            ax1.set_ylabel('CCS', fontsize=18)
            
            if classified.shape[0] > 1:
                b, m = polyfit(classified['M/Z'], classified['Predicted CCS'], 1)
                ax1.plot(classified['M/Z'], b + m * classified['M/Z'], '-', color=color)
        
        ax1.legend(prop={"size":16})
        fig.savefig('./Figures/Figure_{}_{}.png'.format(dataset, tool), facecolor='w')
        plt.show()
        plt.clf()

for dataset in datasets:
    joined=pd.read_csv('./{}/data_classified.csv'.format(dataset), sep=';')

    fig = plt.figure(figsize=(16, 9))
    plt.rcParams['font.size'] = '18'

    fig.suptitle('Classifications for original CCS values for the {} data set'.format(dataset.upper()), fontsize=22)

    ax1 = fig.add_subplot(111)
    
    for clas, color in zip(classes, colors):

        classified=joined.loc[joined[clas] == True]

        ax1.scatter(classified['M/Z'],classified['CCS'], s=5,label='{}'.format(clas), color=color)
        ax1.set_xlabel('M/Z', fontsize=18)
        ax1.set_ylabel('CCS', fontsize=18)
        
        if classified.shape[0] > 1:
            b, m = polyfit(classified['M/Z'], classified['CCS'], 1)
            ax1.plot(classified['M/Z'], b + m * classified['M/Z'], '-', color=color)

    ax1.legend()
    fig.savefig('./Figures/Figure_{}.png'.format(dataset), facecolor='w')
    plt.show()
    plt.clf()

for dataset in datasets:
    raw=pd.read_csv('./{}/data_classified.csv'.format(dataset), sep=';')
    data= pd.DataFrame(columns=['Classification', 'Compounds', 'Values'])
    non_classified= raw
    raw_count=raw.drop_duplicates(subset=['SMILES'])
    
    for clas in classes:

        classified=raw.loc[raw[clas] == True]
        non_classified= non_classified.loc[non_classified[clas] != True]
        values=classified.shape[0]
        classified=classified.drop_duplicates(subset=['SMILES'])
        compounds=classified.shape[0]
        d = {'Classification': [clas], 'Compounds': ['{}/{}'.format(compounds, raw_count.shape[0])], 'Values':['{}/{}'.format(values, raw.shape[0])]}
        df = pd.DataFrame(data=d)
        data = pd.concat([data, df])
    
    values=non_classified.shape[0]
    non_classified=non_classified.drop_duplicates(subset=['SMILES'])
    compounds=non_classified.shape[0]
    d = {'Classification': 'Other', 'Compounds': ['{}/{}'.format(compounds, raw_count.shape[0])], 'Values': ['{}/{}'.format(values, raw.shape[0])]}
    df = pd.DataFrame(data=d)
    data = pd.concat([data, df])
    
    data=data.replace(to_replace='Steroids', value='Steroids and steroid derivatives')
    data=data.replace(to_replace='Nucleoside_nucleotide', value='Nucleosides, nucleotides, and analogues')
    data=data.replace(to_replace='Fatty_acids', value='Fatty acids and conjugates')
    data=data.replace(to_replace='Acyl_carnitines', value='Acyl carnitines')
    data=data.replace(to_replace='Carboxylic_acids', value='Carboxylic acids and derivatives')
    data=data.replace(to_replace='Benzene', value='Benzene and substituted derivatives')
    
    dfi.export(data, './Classifications/{}.png'.format(dataset))

