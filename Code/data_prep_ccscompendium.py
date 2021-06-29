import pandas as pd
import numpy as np
import sys
import os


inchi=pd.read_csv('inchi_originaldata_ccscompendium.tsv', sep='\t')
smiles=pd.read_csv('originaldata_ccscompendium.csv', sep=';')
smiles=smiles[["InChi", "SMILES"]]

inchi= inchi.rename(columns={'SMI': 'SMILES', 'Compound':'Name', 'Ion.Species':'Adduct', 'Theoretical.mz':'M/Z', 'Sources':'Reference' })

data= pd.merge(inchi, smiles, on='InChi')

data=data[["Name", "InChi", "SMILES", "Adduct", "CCS", "M/Z", "Reference"]]

data = data.replace(to_replace ='[M+H]', value = '[M+H]+', regex = False)
data = data.replace(to_replace ='[M+Na]', value = '[M+Na]+', regex = False)
data = data.replace(to_replace ='[M-H]', value = '[M-H]-', regex = False)
data = data.replace(to_replace ='[M+NH4]', value = '[M+NH4]+', regex = False)
data = data.replace(to_replace ='[M+K]', value = '[M+K]+', regex = False)
data = data.replace(to_replace ='[M+]', value = '[M]+', regex = False)
data = data.replace(to_replace ='[M-]', value = '[M]-', regex = False)
data = data.replace(to_replace ='[M-2H]', value = '[M-2H]2-', regex = False)
data = data.replace(to_replace ='[M+H-H2O]', value = '[M+H-H2O]+', regex = False)
data = data.replace(to_replace ='[M+HCOO]', value = '[M+HCOO]-', regex = False)


if not os.path.exists('./ccscompendium'):
    os.makedirs('./ccscompendium')

data.to_csv('./ccscompendium/dataset_ccscompendium.csv', sep=';', index=False)