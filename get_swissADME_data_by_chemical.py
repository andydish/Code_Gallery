import requests
import pandas as pd
import re


# provide dictionary with drugs as keys and their smiles as values
def make_chem_string(chems_smiles_dict):
    chems_smiles_list = []
    for key in chems_smiles_dict.keys():
        smiles = chems_smiles_dict[key]
        smile_drug_pair = str(smiles) + ' ' + str(key)
        chems_smiles_list.append(smile_drug_pair)
    return '\r\n'.join(chems_smiles_list)


def make_request(chem_string):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.swissadme.ch'
    }

    data = {
        'smiles': chem_string,
    }

    response = requests.post('http://www.swissadme.ch/index.php', headers=headers, data=data)

    print('data get code: ' + str(response))

    # Use regular expressions to find the CSV code
    match = re.search(r'results/(\d+)/swissadme\.csv', response.text)
    if match:
        csv_code = match.group(1)
    else:
        raise ValueError("CSV code not found in the response")

    # Download the CSV file
    csv_file = requests.get('http://www.swissadme.ch/results/' + csv_code + '/swissadme.csv')

    print('file get code: ' + str(response))

    # Save the CSV file
    with open('adme_test.csv', 'wb') as file:
        file.write(csv_file.content)

if __name__ == '__main__':
    test_dict = {
        'Ibuprofen': "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
    }

    chem_string = make_chem_string(test_dict)
    make_request(chem_string)
