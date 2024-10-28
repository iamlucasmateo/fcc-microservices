import os
import requests

from dotenv import load_dotenv

from app_logger import get_logger

load_dotenv()
logger = get_logger(__name__)


AUTH_SERVICE_URL = f"http://{os.environ.get('AUTH_SERVICE_ADDRESS')}/login"

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Missing basic auth credentials", 401)
    
    logger.debug("Authorization available")
    basicAuth = (auth.username, auth.password)

    response = requests.post(AUTH_SERVICE_URL, auth=basicAuth)
    logger.debug(f"Authorization response code: {response.status_code}")
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)