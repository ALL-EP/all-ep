import requests
import json
import pprint

# Please refer to "https://docs.gdc.cancer.gov/API/Users_Guide/Data_Analysis/" for more information
# about API endpoints and a complete list of available fields

files_endpt = 'https://api.gdc.cancer.gov/cases'

fields = [
    'case_id',
    'project.project_id',
    'demographic.demographic_id',
    'demographic.ethnicity',
    'demographic.gender',
    'demographic.race',
    'demographic.days_to_death',
    'demographic.days_to_birth',
    'demographic.year_of_birth',
    'demographic.year_of_death',
    'diagnoses.age_at_diagnosis',
    'diagnoses.classification_of_tumor',
    'diagnoses.tumor_grade',
    'diagnoses.tumor_stage',
    'diagnoses.primary_diagnosis',
    'files.data_format',
    'files.file_id',
    'files.file_name'
    ]

fields = ','.join(fields)

filters = {
    'op': 'and',
    'content':[
        {
            'op': 'in',
            'content':{
                'field': 'cases.project.project_id',
                'value': 'TARGET-ALL-P2'
                }
        },
        {
            'op': 'in',
            'content': {
                'field': 'files.experimental_strategy',
                'value': 'WXS'
                }
        }
        ]
    }

params = {
    'filters': json.dumps(filters),
    'fields': fields,
    'format': 'JSON',
    'size': 784,
    'pretty': 'true'
    }

response = requests.get(files_endpt, params = params)
items = json.loads(response.text)

new_dict = { }

# appends only VCF files to each case_id
for item in items['data']['hits']:
    try:
        new_dict[item['case_id']] = [item['demographic'], item['project'], item['diagnoses']]
    except:
        continue
    for file in item['files']:
        if file['data_format'] == 'VCF'and 'MuSE.somatic_annotation' in file['file_name']:
            temp_file_name = file['file_name'].split('.')[0]
            new_dict[item['case_id']].append({"file_name":temp_file_name})

# outputs api data into a json file
with open('dictNames.json', 'w') as f:
    json.dump(new_dict, f)





























