import pandas as pd
import numpy as np


df=pd.read_csv('./resultsdeepccs_raw.csv', sep=',')
df= df.rename(columns={'CCS_DeepCCS': 'Predicted CCS', 'Adducts':'Adduct'})


df = df.replace(to_replace ='M+H', value = '[M+H]+', regex = False)
df = df.replace(to_replace ='M+Na', value = '[M+Na]+', regex = False)
df = df.replace(to_replace ='M-H', value = '[M-H]-', regex = False)
df = df.replace(to_replace ='M-2H', value = '[M-2H]2-', regex = False)

#print(df)

df.to_csv('./resultsdeepccs.csv', index=False)