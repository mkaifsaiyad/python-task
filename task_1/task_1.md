# Step-1: Create New Virtual Environment
##
    python -m venv .venv
***
# Step-2: Activate a Virtual Environment
**For Windows**
##
    source venvName/Scripts/activate
***
# Step-3: Saving Dependencies in a text file
##
    requests==2.32.3 # exact version
    fastapi>=0.115.8,<1.0 # allowing minor/patch updates
    flask>=3.1.0 # greater then specified version
***
# Step-4: Verify Requests Module Installation
##
    import requests

    try:
        request_version = requests.__version__
        print(request_version)
    except:
        print('Module not found')
    else:
        print('Module is present')
***