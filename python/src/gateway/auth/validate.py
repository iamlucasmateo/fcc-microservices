import os, requests

AUTH_SERVICE_URL = f"http://{os.environ.get('AUTH_SERVICE_ADDRESS')}/validate"

def token(request):
    if not "Authorization" in request.headers:
        return None, ("Missing Authorization in Headers", 401)
    
    token = request.headers["Authorization"]

    if not token:
        return None, ("No token in Authorization headers", 401)
    
    response = requests.post(AUTH_SERVICE_URL, headers={"Authorization": token})

    if response.status == 200:
        return response.text, None
    return None, ("Invalid token", 401)