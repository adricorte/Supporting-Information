import pandas as pd
import numpy as np
import sys

file_deprotonated=sys.argv[1]
file_protonated=sys.argv[2]
file_sodiated=sys.argv[3]

deprotonated=pd.read_csv(file_deprotonated, sep='\t')
#print(deprotonated)
deprotonated= deprotonated.rename(columns={'prop_000': 'mz', 'prop_001': 'Predicted CCS'})

adduct_deprotonated=np.repeat('[M-H]-', deprotonated.shape[0])
deprotonated['Adduct']=adduct_deprotonated
#print(deprotonated)


protonated=pd.read_csv(file_protonated, sep='\t')
#print(protonated)
protonated= protonated.rename(columns={'prop_000': 'mz', 'prop_001': 'Predicted CCS'})

adduct_protonated=np.repeat('[M+H]+', protonated.shape[0])
protonated['Adduct']=adduct_protonated
#print(protonated)

sodiated=pd.read_csv(file_sodiated, sep='\t')
#print(sodiated)
sodiated= sodiated.rename(columns={'prop_000': 'mz', 'prop_001': 'Predicted CCS'})

adduct_sodiated=np.repeat('[M+Na]+', sodiated.shape[0])
sodiated['Adduct']=adduct_sodiated
#print(sodiated)

result = pd.concat([deprotonated, protonated, sodiated])
#print(result)

result = result[result['Predicted CCS'].notna()]
#print(result.shape)

result.to_csv('./resultsdarkchem.csv', sep=',', index=False)


