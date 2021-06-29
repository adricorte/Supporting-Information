import pandas as pd
import numpy as np
import os
import sys


tool=sys.argv[1]
database=sys.argv[2]
file_original=sys.argv[3]
file_results=sys.argv[4]

original=pd.read_csv(file_original, sep=';')
results=pd.read_csv(file_results, sep=',')

original= original.rename(columns={'SMI': 'SMILES'})
results=results.rename(columns={'adduct': 'Adduct', 'pred_ccs':'Predicted CCS','mz':'Predicted_mz'})
joined=pd.merge(original, results, on=['SMILES', 'Adduct'])
joined = joined.drop(['Name_y', 'SMILES_canonical', 'status', 'rss', 'monoisotopic_mass', 'name'], axis=1, errors='ignore')

#print(joined)
joined["difference"] = joined["CCS"] - joined["Predicted CCS"]
#print(joined)

mean_error= np.mean(np.abs(joined.difference))
desv_error= np.std(np.abs(joined.difference))
#print(mean_error, desv_error)

joined= joined.rename(columns={'Name_x': 'Name'})


joined["percentage_difference"] = joined["difference"]*100/joined["CCS"]

#print(joined)
mean_percentage_error= np.mean(np.abs(joined.percentage_difference))
desv_percentage_error= np.std(np.abs(joined.percentage_difference))
#print(mean_percentage_error, desv_percentage_error)

joined.to_csv('joined{}.csv'.format(tool), sep=';', index=False)

cwd = os.getcwd()

outliers10=joined[(joined.percentage_difference>=10) | (joined.percentage_difference<=-10)]


d = {'Dataset': [database],'Tool': [tool], 'Mean_abs': [mean_error], 'SD_abs': [desv_error], 'Mean_perc': [mean_percentage_error], 'SD_perc': [desv_percentage_error], 'Outliers': [outliers10.shape[0]]}
df = pd.DataFrame(data=d)
df.to_csv('metrics{}.csv'.format(tool), sep=';', index=False)


text = "Report:\n\nTool: {} \nDataset: {} \n\n\tMean error: {} \n\tStandar Deviation error: {}\n\tMean percentage error: {} \n\tStandar Deviation percentage error: {} \n\t Outliers: {} \n\n".format(tool, database, mean_error, desv_error, mean_percentage_error, desv_percentage_error, outliers10.shape[0])
#print(text)
with open(os.path.join(cwd, 'report{}.txt'.format(tool)),'w') as savefile:
    savefile.write(text)
