import urllib.request,urllib.error
import urllib.parse
import requests
import os
import csv
import json
from rdkit import Chem 
import pandas as pd
from colorama import Fore
from IPython.display import display, HTML
import traceback
import numpy as np
import time


def post_query_classyfire(smiles):
    '''
    :param smiles: smiles structure of the compound
    :type string
    
    '''
    Glycerolipids=""
    Glycerophospholipids=""
    Sphingolipids=""
    Steroids=""
    Nucleoside_nucleotide=""
    Fatty_acids=""
    Acyl_carnitines=""
    Monosaccharides=""
    Carboxylic_acids=""
    Benzene=""
        

    # Primero -> calcular INCHI KEY
    mol = Chem.MolFromSmiles(smiles) 
    inchi = Chem.MolToInchi(mol) 
    inchi_key=Chem.inchi.InchiToInchiKey(inchi)
    #print(inchi_key)


    #inchi_key = 'SBJKKFFYIZUCET-JLAZNSOCSA-N' # ASUMIR CORRECTITUD. CUIDADO CON INICIO DE STRING INCHIKEY=
    # SEGUNDO -> get entity from inchi key

    urlEntity="http://classyfire.wishartlab.com/entities/" + inchi_key + ".json"
    
    try:
        # IF OK -> return properties

        with urllib.request.urlopen(urlEntity) as classyfireContent:
            classyfireString = classyfireContent.read().decode('utf-8')
            obj = json.loads(classyfireString)
            
            try:
                smiles=obj["smiles"]
                
                ancestors= obj["ancestors"]
                
                if 'Glycerolipids' in ancestors:
                    Glycerolipids=True
                if 'Glycerophospholipids' in ancestors:
                    Glycerophospholipids=True
                if 'Sphingolipids' in ancestors:
                    Sphingolipids=True
                if 'Steroids and steroid derivatives' in ancestors:
                    Steroids=True
                if 'Nucleosides, nucleotides, and analogues' in ancestors:
                    Nucleoside_nucleotide=True
                if 'Fatty acids and conjugates' in ancestors:
                    Fatty_acids=True
                if 'Acyl carnitines' in ancestors:
                    Acyl_carnitines=True
                if 'Monosaccharides' in ancestors:
                    Monosaccharides=True
                if 'Carboxylic acids and derivatives' in ancestors:
                    Carboxylic_acids=True
                if 'Benzene and substituted derivatives' in ancestors:
                    Benzene=True
                
                                
            except TypeError as e:
                print(Fore.RED +'\t no smiles ')
                pass
            except Exception as e:
                print(Fore.GREEN +'\t no smiles ')
                pass
            
    except urllib.error.HTTPError as httpe:
        
        error_code = httpe.code
        print(Fore.RED +"error CODE=", error_code)
        
        if(error_code == 429):
            print("DENTRO")
            time.sleep(30)
            Glycerolipids, Glycerophospholipids, Sphingolipids, Steroids, Nucleoside_nucleotide, Fatty_acids, Acyl_carnitines, Monosaccharides, Organic_acids, Carboxylic_acids, Benzene=post_query_classyfire(smiles)
        
        else:
            print(inchi, "\t", inchi_key, " -> ", httpe)

            # IF NOT OK -> POST QUERY WITH SMILES
            urlQueriesClassyfire = "http://classyfire.wishartlab.com/queries.json"
            label = 'my_label' + str(inchi_key)
            # data = urllib.parse.urlencode({'inchi': inchi, 'label': label, 'query_type': 'STRUCTURE'})
            # data = data.encode('ascii')
            data = {"query_input": smiles, "label": label, "query_type": "STRUCTURE"}
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            #print(data,headers)
            try:
                r = requests.post(url = urlQueriesClassyfire, data = json.dumps(data), headers = headers)
                print(r.text)
            except Exception as e:
                traceback.print_exc()
                print(e)
        

        # GET THE QUERY ID
        
        # GET ENTITY AFTER N SECONDS (30)
        
    except Exception as e:
        print(Fore.RED + "\t general exception: ")
        traceback.print_exc()

    finally:
        # cerrar recursos (ficheros)
        return Glycerolipids, Glycerophospholipids, Sphingolipids, Steroids, Nucleoside_nucleotide, Fatty_acids, Acyl_carnitines, Monosaccharides, Carboxylic_acids, Benzene

def main():

    datasets=['allccs']
    
    for dataset in datasets:
        
        data_raw= pd.read_csv('./../Predictions_datasets/{}/dataset_{}.csv'.format(dataset, dataset), sep=';')
        data= data_raw[["Name", "SMILES"]]
        data= data.drop_duplicates('SMILES')

        data["Glycerolipids"] = ""
        data["Glycerophospholipids"] = ""
        data["Sphingolipids"] = ""
        data["Steroids"] = ""
        data["Nucleoside_nucleotide"]=""
        data["Fatty_acids"] = ""
        data["Acyl_carnitines"] = ""
        data["Monosaccharides"] = ""
        data["Carboxylic_acids"] = ""
        data["Benzene"] = ""


        for index, row in data.iterrows():
            
            smiles_row=row['SMILES']

            if isinstance(smiles_row, float):

                print(Fore.BLUE + "\t NO SMILES")
                continue
            else:
                time.sleep(5)
                Glycerolipids, Glycerophospholipids, Sphingolipids, Steroids, Nucleoside_nucleotide, Fatty_acids, Acyl_carnitines, Monosaccharides, Carboxylic_acids, Benzene= post_query_classyfire(smiles_row)

                data.loc[index, 'Glycerolipids']=Glycerolipids
                data.loc[index, 'Glycerophospholipids']=Glycerophospholipids
                data.loc[index, 'Sphingolipids']=Sphingolipids
                data.loc[index, 'Steroids']=Steroids
                data.loc[index, 'Nucleoside_nucleotide']=Nucleoside_nucleotide
                data.loc[index, 'Fatty_acids']=Fatty_acids
                data.loc[index, 'Acyl_carnitines']=Acyl_carnitines
                data.loc[index, 'Monosaccharides']=Monosaccharides
                data.loc[index, 'Carboxylic_acids']=Carboxylic_acids
                data.loc[index, 'Benzene']=Benzene

        data.to_csv('./../Predictions_datasets/{}/classifications.csv'.format(dataset), sep=';', index=False)

    
if __name__=="__main__":
    main()