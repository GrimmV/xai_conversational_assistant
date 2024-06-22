import requests
import urllib.parse
from acronyms import acronyms

base_url = "http://localhost:5001"
base_path = "/api/v1"

def get_data(directory, key_word, params):
    # Convert list values in params to repeated parameters
    expanded_params = []
    for key, value in params.items():
        if isinstance(value, list):
            for item in value:
                expanded_params.append((key, item))
        else:
            expanded_params.append((key, value))
    
    expanded_params.append(("index", "1"))

    acronym = acronyms[key_word]

    if acronym == "datapoint":
        directory = "data"
    if acronym == "context":
        directory = "xai"
    url = f'{base_url}{base_path}/{directory.lower()}/{acronym}?' + urllib.parse.urlencode(expanded_params)
    print(url)
    data_raw = requests.get(url)
    data_raw.raise_for_status()
    data = data_raw.json()

    return data