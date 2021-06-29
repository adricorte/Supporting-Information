import pandas as pd
import numpy as np
import sys
import os


df=pd.read_csv('originaldata_cembio.csv', sep=';')

#print(df)

df2=df[["Lipid Name", "SMILES", "Adduct", " Experimental CCS ", "m/z"]]

df2= df2.rename(columns={' Experimental CCS ':'CCS', 'Lipid Name':'Name', 'm/z':'M/Z'})
#print(df2)

if not os.path.exists('./cembio'):
    os.makedirs('./cembio')

df2.to_csv('./cembio/dataset_cembio.csv', sep=';', index=False)