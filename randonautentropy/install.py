import os
import shutil

def install():
    """
    Tries to fetch TemporalLib from GitHub and build it

    """
    print("TemporalLib not found. Attempting to install it...")
    print("==================================================")
    module_path = os.path.abspath(os.path.dirname(__file__))
    temporal_path = os.path.abspath(f"{module_path}/temporal")
    os.chdir(module_path)
    try:
        os.system('git clone --depth 1 git@github.com:TheRandonauts/temporal.git')
    except:
        print("Cloning Temporal from GitHub failed. Please install it manually:")
        return
    try:
        os.chdir(temporal_path)
        os.system('./make.sh')
        print("Installed. Deleting build directory.")
        shutil.rmtree(temporal_path, ignore_errors=True)
    except:
        print("Compiling Temporal failed. Please install it manually:")
        return
    print("==================================================")
    print("TemporalLib successfully installed")