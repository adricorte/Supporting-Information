import pandas as pd
import numpy as np
import sys
import os


df=pd.read_csv('originaldata_ccsbase.csv', sep=';')

df2=df[["Name", "SMI", "Adduct", "CCS", "M/Z", "Ref"]]

df2= df2.rename(columns={'Ref':'Reference', 'SMI':'SMILES'})
#print(df2)

if not os.path.exists('./ccsbase'):
    os.makedirs('./ccsbase')

df2.to_csv('./ccsbase/dataset_ccsbase.csv', sep=';', index=False)