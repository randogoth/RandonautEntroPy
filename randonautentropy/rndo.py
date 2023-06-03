import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import json

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

URL = 'https://qrng.randonautica.com/api/json/'
typeS = {
    'int32' : 'randint32', 
    'hex16' : 'randhex', 
    'uniform' : 'randuniform',
    'normal' : 'randnormal',
    'base64' : 'randbase64'
}

DEVICE_ID = 'QWR70154'

def get(length=10, type='hex16'):
    """
    Fetch data from the Randonautica Quantum Random Numbers JSON API
    
    length (int):  length of bytes to get from the QRNG when `type=hex16`
    type (string): type of random number data to fetch. 
                   Valid choices are `hex16`, `int32`, `uniform`, `normal`, `base64`

    """
    if type not in typeS.keys():
        raise Exception("type must be one of %s" % typeS.keys())
    url = URL + typeS[type] + '?' + urlencode({
        'device_id': DEVICE_ID,
        'length': length,
    })
    data = __get_json(url)
    return data


def __get_json(url):
    return requests.get(url, verify=False).json()