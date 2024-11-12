import requests

from api.cookieTokenManager import get_tokens, refresh_access_token, logout
from api.cookieTokenManager import url

def make_authenticated_request(endpoint, method="get", data=None):
    tokens = get_tokens()

    access_token = tokens['access_token']

    if not access_token:
        return {"status_code":500, "detail":"Not Authenticated, Please Log In"}
        
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        if method.lower() == "get":
            response = requests.get(url + endpoint, headers=headers)
        elif method.lower() == "post":
            response = requests.post(url + endpoint, headers=headers, json=data)
        print(response.status_code)

        # If token expired, try to refresh
        if response.status_code == 403: 
            if refresh_access_token():
                response = make_authenticated_request(endpoint, method, data)  # Retry request with new token
            else:
                #logout()
                return {"status_code":500, "detail":"Session expired, Please Log In"} # If refresh failed, logout

        return response
        
    except requests.exceptions.RequestException as e:
        return {"status_code":500, "detail": str(e)}