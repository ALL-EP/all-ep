## Exploring differences in tumor mutation burden in acute lymphoblastic leukemia among Hispanic and non-Hispanic subsets

The purpose of this study is to explore differences in tumor mutation burden in Acute Lymphoblastic Leukemia among Hispanic and non-Hispanic patient subsets. In particular, TMB differences within gene ontology terms of ALL types and within white, non-Hispanic and Hispanic groups are explored.

## Description of scripts in this repository:
### main.py
Parses an input reference file (ref.txt) consisting of a list of genes with intron and exon start and stop sites. Only exons were included in this study.  Calculates the length of the coding region for each gene.

### api.py
Filters pertaining to relevant clinical and demographic data are applied to the 'https://api.gdc.cancer.gov/cases' endpoint. VCF files ids are appended to each case id and added to a dictionary.

### bins.py
Tumor mutation data was downloaded from the GDC portal for the TARGET-ALL-P2 study. The input file was fed into UTEP's Oncominer pipieline (https://oncominer.utep.edu/) and the output file 'all_comb.csv' was used for further processing. Tumor mutation burden is calculated for each gene and a comprehensive dictionary combining all VCF and TMB data is created for each case id.

### goterms.py and goterms_cont.py
Using two reference files goInfo-hs.txt and geneDict-hs.txt, a list of genes associated with each Gene Ontology term (http://geneontology.org/) was compiled for reference. Outputs a list of GO terms, associated genes and gene tmb for each case_id. Cumulative TMB for each GO term is also calculated.

## Versioning:
pandas v 1.2.4  
numpy v 1.20.3  
matplotlib v 3.4.2  
scipy v 1.7.3

## References
Please refer to "https://docs.gdc.cancer.gov/API/Users_Guide/Data_Analysis/" for more information about API endpoints and a complete list of available fields  

Please refer to https://portal.gdc.cancer.gov/ for accessing The Cancer Genome Atlas (TCGA) portal.   

The Oncominer pipeline accepts an Oncominer input file (OMI). For more information on submitting jobs to this server and input file formats, please refer to https://oncominer.utep.edu/




