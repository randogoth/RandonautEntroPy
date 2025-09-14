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

    Non-breaking behavior:
      - length is ONLY used for type='hex16' (number of hex BYTES).
      - All other types return exactly ONE value.

    Returns by type:
      - 'uniform' -> float in [0,1)
      - 'normal'  -> float (Gaussian)
      - 'int32'   -> signed 32-bit int
      - 'base64'  -> str (single base64 blob)
      - 'hex16'   -> str of length 2*length (hex chars)

    Falls back to local randomness if the API is unavailable or returns
    an unexpected shape.
    """
    if type not in typeS:
        raise Exception("type must be one of %s" % list(typeS.keys()))

    # Build URL. `length` only meaningful for hex16; QRNG ignores it for others.
    params = {'device_id': DEVICE_ID}
    if type == 'hex16':
        params['length'] = int(length)

    url = URL + typeS[type] + '?' + urlencode(params)

    # Try API first
    try:
        data = __get_json(url, timeout=timeout)
        return _parse_api_value(type, data, length)
    except Exception:
        # Network/parse/shape error -> fallback
        return _fallback_value(type, length)

def __get_json(url, timeout=1.5):
    resp = requests.get(url, verify=False, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

# ----- Helpers -----

def _parse_api_value(t, payload, length):
    """
    Accept common shapes:
      - {"data":[...]}  (usual)
      - bare number/string
      - single-item list
    Enforce return types listed in get() docstring.
    """
    # Helper to pull first item from possible shapes
    def first_item(x):
        if isinstance(x, dict) and "data" in x and x["data"]:
            return x["data"][0] if isinstance(x["data"], list) else x["data"]
        if isinstance(x, list) and x:
            return x[0]
        return x

    if t == 'uniform':
        v = float(first_item(payload))
        if not (0.0 <= v < 1.0):
            raise ValueError("uniform out of range")
        return v

    if t == 'normal':
        return float(first_item(payload))

    if t == 'int32':
        v = int(first_item(payload))
        # normalize to signed 32-bit just in case
        v = ((v + 2**31) % 2**32) - 2**31
        return v

    if t == 'base64':
        v = first_item(payload)
        if not isinstance(v, str):
            # Sometimes APIs deliver bytes; normalize to str
            v = str(v)
        return v

    if t == 'hex16':
        # Expect list of hex bytes or a single hex string; normalize to one string of 2*length chars
        d = payload.get("data", payload) if isinstance(payload, dict) else payload
        if isinstance(d, list):
            s = ''.join(str(b) for b in d)
        else:
            s = str(d)
        # If API returned more/less, trim/pad to exact 2*length for strict non-breaking behavior
        want = max(0, int(length)) * 2
        if len(s) < want:
            # pad with extra local entropy to reach length
            s += secrets.token_hex((want - len(s) + 1) // 2)[:(want - len(s))]
        elif len(s) > want and want > 0:
            s = s[:want]
        return s

    # Shouldn't reach here
    raise ValueError("Unknown type")

def _fallback_value(t, length):
    if t == 'uniform':
        return random.random()
    if t == 'normal':
        return random.gauss(0.0, 1.0)
    if t == 'int32':
        u = secrets.randbits(32)
        # signed 32-bit
        return u - (1 << 32) if (u & (1 << 31)) else u
    if t == 'base64':
        # 16 random bytes
        return base64.b64encode(os.urandom(16)).decode('ascii')
    if t == 'hex16':
        # exactly `length` bytes -> 2*length hex chars
        return secrets.token_hex(int(length))
    # Shouldn't reach here
    raise ValueError("Unknown type")
