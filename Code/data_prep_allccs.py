import pandas as pd
import numpy as np
import sys
import os
from IPython.display import display, HTML

df=pd.read_csv('originaldata_allccs.csv', sep='\t')

df2=df[["name", "smiles", "adduct", "ccs", "mz"]]

df2= df2.rename(columns={'ccs':'CCS', 'name':'Name', 'smiles':'SMILES','mz':'M/Z', 'adduct':'Adduct'})
#print(df2)

if not os.path.exists('./allccs'):
    os.makedirs('./allccs')

df2.to_csv('./allccs/dataset_allccs.csv', sep=';', index=False)