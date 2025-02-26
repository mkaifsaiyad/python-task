import pip
import subprocess
import sys

def install(n, v):
    subprocess.call([sys.executable, '-m', 'pip', 'install', f'{n}=={v}'])
    import requests
    if requests.__version__ != v:
        print('\nVersion missmatch')
    else:
        print(f"\nmodule {n} version {v} installed and imported successfully!")

# def install_and_check(package):
#     pip.main(['install', package])

# install_and_check('pandas')
version = input('provide version of requests: ')

install('requests',version)