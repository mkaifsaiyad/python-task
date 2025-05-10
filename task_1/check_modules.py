import requests

try:
    request_version = requests.__version__
    print(request_version)
except:
    print('Module not found')
else:
    print('Module is present')