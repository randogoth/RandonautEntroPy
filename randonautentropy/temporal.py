import os
import shutil
from subprocess import check_output as exec
from .install import install

def get(length=10, channel=0):
    length *= 2
    module_path = os.path.abspath(os.path.dirname(__file__))
    temporal_path = os.path.abspath(f"{module_path}/temporal")
    exe_path = f'{temporal_path}/result/{os.uname().sysname}/temporal'
    if shutil.which('temporal') is None:
       install()
    temporal = exec(f'temporal hexdump {channel} {length}', shell=True)
    return temporal[:-1].decode('UTF-8')