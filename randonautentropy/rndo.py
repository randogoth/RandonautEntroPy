# Copyright 2023 randogoth <tobias@randonauts.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
A Python interface to the Randonautica Quantum Random Numbers Server.

"""

import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import json

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

VERSION = '1.0.0'
URL = 'https://api.qrng.rndo.it/api/json/'
typeS = {
    'int32' : 'randint32', 
    'hex16' : 'randhex', 
    'uniform' : 'randuniform',
    'normal' : 'randnormal',
    'base64' : 'randbase64'
}

DEVICE_ID = 'QWR70154'

def get(type='hex', length=1):
    """Fetch data from the Randonautica Quantum Random Numbers JSON API"""
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