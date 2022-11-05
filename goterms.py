import pprint
import pandas as pd # version 1.2.4
import numpy as np # version 1.20.3
from collections import defaultdict
import json
from bins import api_tmb_mapped

# "gooutput.txt" containts a list of all GO terms and associated genes
# please refer to "http://geneontology.org/" for more information
f = open("gooutput.txt", "r", encoding='latin1')
lines = f.readlines()
f.close()

api_tmb_mapped_go_terms = {}
api_tmb_mapped_go_terms = defaultdict(list)


for key in api_tmb_mapped:
    count = 0;
    try:
        patient_genes = api_tmb_mapped[key][1]
        for line in lines:
            list = line.split(">>>")
            try:
                go_term = list[0]
                genes = list[1].rstrip().split(",")
                for gene in patient_genes:
                    if gene[0] in genes:
                        count += 1
                        if count > len(genes) / 2: #ignore GO terms that have a greater than 50% overlap with patient genes
                            continue;
                        api_tmb_mapped_go_terms[key].append([go_term, gene[0], gene[1]])
            except:
                continue;

    except:
        continue;


# outputs a list of go terms, associated genes and gene tmb for each case_id
with open('go_terms_full_dataset.txt', 'w') as f:
    pprint.pprint(api_tmb_mapped_go_terms, stream = f)