import pandas as pd
import numpy as np


df=pd.read_csv('./datadeepccs.csv', sep=',')
#print(df)

df=df[df["SMILES"].str.contains("8")==False]
df=df[df["SMILES"].str.contains("Fe")==False]
df=df[df["SMILES"].str.contains("s")==False]
df=df[df["SMILES"].str.contains("As")==False]
df=df[df["SMILES"].str.contains("Cn")==False]
df=df[df["SMILES"].str.contains("o")==False]

#print(df)

df.to_csv('./datadeepccs_corrected.csv', index=False)