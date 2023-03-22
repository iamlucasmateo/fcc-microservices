import os
import requests


AUTH_SERVICE_URL = f"http://{os.environ.get('AUTH_SERVICE_ADDRESS')}/login"

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Missing basic auth credentials", 401)
    
    basicAuth = (auth.username, auth.password)

    response = requests.post(AUTH_SERVICE_URL, auth=basicAuth)

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)