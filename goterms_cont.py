from collections import defaultdict
from goterms import api_tmb_mapped_go_terms

copy= {}
copy = defaultdict(list)

# creates an accessory dictionary with a single, aggregate tmb value for each go term
for key in api_tmb_mapped_go_terms:
    temp_dict = {}
    vals = api_tmb_mapped_go_terms[key]
    for val in vals:
        go_term = val[0]
        tmb = val[2]
        if go_term in temp_dict:
            # add tmb values of all genes in a GO term
            temp_dict[go_term] = temp_dict[go_term] + tmb
        else:
            temp_dict[go_term] = tmb
    copy[key] = temp_dict





