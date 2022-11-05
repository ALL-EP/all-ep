import pprint
import pandas as pd
import numpy as np
from collections import defaultdict
import json
from goterms import api_tmb_mapped_go_terms
from bins import api_tmb_mapped
from scipy import stats


genes_list= []
for key in api_tmb_mapped:
    genes = api_tmb_mapped[key][-1]
    for gene in genes:
        # print(gene[0])
        if gene[0] not in genes_list:
            genes_list.append(gene[0])

# print(genes_list)


significant_genes = []
for gene in genes_list:
    hispanic_genes = []
    nonhispanic_genes = []
    for key in api_tmb_mapped:
        try:
            ethnicity = api_tmb_mapped[key][0][0]["ethnicity"]
            patient_genes = api_tmb_mapped[key][-1]
            for pt_gene in patient_genes:
                if ethnicity == 'hispanic or latino':
                    if gene == pt_gene[0]:
                        hispanic_genes.append(pt_gene[1])
                        # print(key, term, pt_gene[0])
                    else:
                        hispanic_genes.append(0)
                if ethnicity == 'not hispanic or latino':
                    if gene == pt_gene[0]:
                        nonhispanic_genes.append(pt_gene[1])
                        # print(key, term, pt_genes[0])
                    else:
                        nonhispanic_genes.append(0)
        except:
            continue;
    group1 = np.array(hispanic_genes)
    group2 = np.array(nonhispanic_genes)
    # print(group1.mean())
    # print(group2.mean())
    # print(np.var(group1))
    # print(np.var(group2))
    result = stats.ttest_ind(a=group1, b=group2, equal_var=True)
    # print(result[1])
    if result[1] < .05:
        # print(gene)
        # print(group1.mean())
        # print(group2.mean())
        # print(np.var(group1))
        # print(np.var(group2))
        # print(result[1])
        significant_genes.append(gene)
#     # print("hispanic", hispanic_go_terms)
#     # print("nonhispanic", nonhispanic_go_terms)

# print(len(genes_list))
# print(len(significant_genes))
#
# with open('genes_significant.txt', 'w') as f:
#     pprint.pprint(significant_genes, stream = f)