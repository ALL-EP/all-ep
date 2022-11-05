import pprint
import pandas as pd # version 1.2.4
import numpy as np # version 1.20.3
from collections import defaultdict
import json
import csv

apilink = {}
apilink = defaultdict(list)

# Please see the readme file for information about "all_comb.csv" and using the oncominer pipeline
df = pd.read_csv ('all_comb.csv', sep='\t')
df1 = df.iloc[:, np.r_[11,12,19:1241]]
cleaned = df1[df1['where_in_transcript'].str.contains('CDS')]


#read in the output file generated by main.py
f = open("output.txt", "r", encoding='latin1')
lines = f.readlines()
f.close()

#add all gene names and CDS length to a dictionary
CDS = {}
allvals = lines[0].split(",")
for item in allvals:
    item1 = item.split(":")
    gene_name = item1[0].replace("'","").strip(" ")
    temp = item1[1].replace("'","").strip(" ")
    CDS_number = temp.replace("'","").strip(" ")
    CDS[gene_name] = CDS_number

# read in the output file  produced by api.py
with open('dictNames.json') as f:
    apilink = json.load(f)
    # pprint.pprint(apilink)

# temporary dicts
new_dict = {}
final_dict = {}
tmb_dict = {}
new_dict = defaultdict(list)
final_dict = defaultdict(list)
tmb_dict = defaultdict(list)

# process dataframe containing data from "all_comb.csv"
for index, row in cleaned.iterrows():
    val1 = row[0]
    val2 = row[1]
    val3 = [row[2:1241]]
    val4 = [val3[0][::2]] # extract only tumor patients and ignore controls
    strreplace = val1[1:-1].replace("'", "")
    splitlist = strreplace.split(", ")
    strreplace1 = val2[1:-1].replace("'", "")
    splitlist2 = strreplace1.split(", ")
    for item, item1 in zip(splitlist, splitlist2):
        new_dict[item].append(item1)
    new_dict[item].append(val4)


for key in new_dict:
    vals = new_dict[key]
    last_obj = vals[-1][0]
    if 'CDS' in vals:
        final_dict[key].append(last_obj)


zipVals =[]
# calculate tmb for each gene ( number of mutations/CDS length)
for k, v in final_dict.items():
    if k in CDS.keys():
        if type(v[0]) is not str and int(CDS[k]) != 0:
                file_name = v[0].index.tolist()
                file_vals = v[0].tolist()
                zipVals = list(zip(file_name, file_vals))
                for a,b in zipVals:
                    temp_file_name = a.split('.')[0]
                    tmb = int(b)/int(CDS[k])
                    if(tmb > 0.0) : # ignore tmb values that are 0
                        temp_list = [k, tmb]
                        tmb_dict[temp_file_name].append(temp_list)


# final dict containing case_id with associated sociodemographic info, file ids
# as well as a list of genes and tmb values for each case_id
api_tmb_mapped = {}
api_tmb_mapped = defaultdict(list)


# append all vcf file names to associated case_id
for patient in apilink:
    try:
        if apilink[patient][3]['file_name'] in tmb_dict.keys():
            api_tmb_mapped[patient].append(apilink[patient])
            api_tmb_mapped[patient].append(tmb_dict[apilink[patient][3]['file_name']])
        if apilink[patient][4]['file_name'] in tmb_dict.keys():
            api_tmb_mapped[patient].append(tmb_dict[apilink[patient][4]['file_name']])
    except:
        continue;

