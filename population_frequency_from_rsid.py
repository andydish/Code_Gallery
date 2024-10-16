import pandas as pd
import requests
from io import StringIO
import json

def FVIND(d, target_key):
    # finds the value of a key in a nested dictionary
    if target_key in d:
        return d[target_key]
    for key, value in d.items():
        if isinstance(value, dict):
            result = FVIND(value, target_key)
            if result is not None:
                return result
    return None

def get_allele_frequency(rsid):
    rsid_fetch = rsid.split("_")[0] # remove things like _a to be able to search
    response = requests.get(f'https://api.ncbi.nlm.nih.gov/variation/v0/refsnp/{rsid_fetch}/frequency')
    if response.status_code == 200:
        json_string = response.content.decode('utf-8')
        json_string = json_string.replace('SAMN10492705', 'Total')
        json_string = json_string.replace('SAMN10492703', 'African')
        json_string = json_string.replace('SAMN10492704', 'Asian')
        json_string = json_string.replace('SAMN10492696', 'African Others')
        json_string = json_string.replace('SAMN10492698', 'African American')
        json_string = json_string.replace('SAMN10492697', 'East Asian')
        json_string = json_string.replace('SAMN10492701', 'Other Asian')
        json_string = json_string.replace('SAMN10492699', 'Latin American 1')
        json_string = json_string.replace('SAMN10492700', 'Latin American 2')
        json_string = json_string.replace('SAMN10492702', 'South Asian')
        json_string = json_string.replace('SAMN10492695', 'European')
        json_string = json_string.replace('SAMN11605645', 'Other')
        data = json.loads(json_string)
        allele_data = FVIND(data, 'allele_counts')
        ref_allele = FVIND(data, 'ref')
        data_for_df = []
        for pop, alleles in allele_data.items():
            total = sum(alleles.values())
            row = {'Population': pop, 'Ref_Allele': ref_allele, 'Ref_Allele_Freq': alleles[ref_allele] / total}
            inst = 0
            for allele, count in alleles.items():
                inst = inst + 1
                if allele != ref_allele:
                    row[f'Alt_Allele_Freq_{inst}'] = count / total
                    row[f'Alt_Allele_{inst}'] = allele
            data_for_df.append(row)
        df = pd.DataFrame(data_for_df, columns=["rsid", "Population",
                                                "Ref_Allele", "Ref_Allele_Freq",
                                                "Alt_Allele_1", "Alt_Allele_Freq_1",
                                                "Alt_Allele_2", "Alt_Allele_Freq_2",
                                                "Alt_Allele_3", "Alt_Allele_Freq_3"])
        df['rsid'] = 'rs' + rsid # adding the rsID back
        return df
    print(f'{rsid} not found or request failed.')
    return None

rsid = '28371725' # no RS number
frequency = get_allele_frequency(rsid)
print(frequency)
