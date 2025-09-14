import requests
import random
import secrets
import base64
import os

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import json

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

URL = 'https://qrng.randonautica.com/api/json/'
typeS = {
    'int32'  : 'randint32',
    'hex16'  : 'randhex',
    'uniform': 'randuniform',
    'normal' : 'randnormal',
    'base64' : 'randbase64'
}

DEVICE_ID = 'QWR70154'

def get(length=10, type='hex16', timeout=1.5):
    """
    Fetch data from the Randonautica Quantum Random Numbers JSON API.
    Falls back to local randomness if the API is unavailable.

    length (int): number of values/bytes to get
    type (str): one of {'hex16','int32','uniform','normal','base64'}
    timeout (float): HTTP timeout in seconds
    """
    if type not in typeS:
        raise Exception("type must be one of %s" % list(typeS.keys()))

    # Try QRNG first
    url = URL + typeS[type] + '?' + urlencode({
        'device_id': DEVICE_ID,
        'length': length,
    })
    try:
        data = __get_json(url, timeout=timeout)
        # Validate expected shape minimally
        if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
            return data
        # If shape unexpected, fall back
    except Exception:
        pass

    # Fallback path: generate locally with best available primitives
    return _fallback_response(type=type, length=length)

def __get_json(url, timeout=1.5):
    resp = requests.get(url, verify=False, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

def _fallback_response(type: str, length: int):
    """
    Produce a response object that mirrors the QRNG API:
    {
      "type": <type>,
      "length": <length>,
      "data": [...],
      "success": true,
      "source": "fallback"
    }
    """
    if type == 'uniform':
        # Uniform floats in [0.0, 1.0)
        data = [random.random() for _ in range(length)]

    elif type == 'normal':
        # Standard normal N(0,1)
        data = [random.gauss(0.0, 1.0) for _ in range(length)]

    elif type == 'int32':
        # 32-bit signed ints (match typical randint32 range: [-2^31, 2^31-1])
        # secrets is preferable to random for stronger entropy.
        data = []
        for _ in range(length):
            u = secrets.randbits(32)
            # Convert to signed 32-bit
            if u & (1 << 31):
                u = u - (1 << 32)
            data.append(u)

    elif type == 'hex16':
        # Hex string of length*2 bytes? The API name suggests 16-bit hex bytes.
        # Historically this endpoint returns hex bytes; emulate by returning a single hex string
        # of 2*length characters (each byte -> 2 hex chars). If API returns list, adapt as needed.
        # Here we return a list of hex byte strings to match "data": [...]
        data = [secrets.token_hex(1) for _ in range(length)]

    elif type == 'base64':
        # Return base64-encoded random bytes; match as a list of base64 strings
        data = []
        for _ in range(length):
            b = os.urandom(16)  # 16 bytes per element; adjust if your API uses a different size
            data.append(base64.b64encode(b).decode('ascii'))

    else:
        # Should never hit due to earlier check
        data = []

    return {
        "type": type,
        "length": length,
        "data": data,
        "success": True,
        "source": "pseudo"
    }