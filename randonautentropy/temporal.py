import os
import shutil
from subprocess import check_output as exec
from .install import install

def get(length=10, channel=0):
    """
    Fetch data from the local TemporalLib RNG and returns a string of hex16
    
    length (int):  length of bytes to get from the RNG
    channel (int): 0 for slower but higher quality entropy, 1 for faster but lower quality entropy

    """
    length *= 2 # returns nibbles by default, so let's make that bytes
    module_path = os.path.abspath(os.path.dirname(__file__))
    temporal_path = os.path.abspath(f"{module_path}/temporal")
    exe_path = f'{temporal_path}/result/{os.uname().sysname}/temporal'
    if shutil.which('temporal') is None:
       install()
    temporal = exec(f'temporal hexdump {channel} {length}', shell=True)
    return temporal[:-1].decode('UTF-8')