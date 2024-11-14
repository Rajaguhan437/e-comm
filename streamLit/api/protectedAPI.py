import requests
import uuid
from api.cookieTokenManager import get_tokens, refresh_access_token, logout
from api.cookieTokenManager import url, cookie_manager

def make_authenticated_request(endpoint, method="get", data=None):
    #tokens = get_tokens()
    
    cookie_data = cookie_manager.get_all()
    if cookie_data['access_token'] == None:
        print()        

    tokens =  {
        "access_token": cookie_data.get("access_token"),
        "refresh_token": cookie_data.get("refresh_token")
    }
    # print(tokens,uuid.uuid4(),"***************************")

    access_token = tokens['access_token']
    # access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1aGFuQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiJDJiJDEyJEVFNzdSMUJwaThSbnAxZEdYbVBQT2V4V1BzTC9tU2xIRnhKd0FVWDY4V1ZBVW10RVlNR29DIiwicm9sZSI6IkN1c3RvbWVyIiwiZXhwIjoxNzMxNDE1MzYxLjc0MDEzNn0.bry3GPpvXtDHgfA0uZIcHIGoilpiiBFWiFnGPXI_rCY"
    if not access_token:
        raise {"status_code":500, "detail":"Not Authenticated, Please Log In"}

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

        return {"status_code":200, "content": response.content}
        
    except requests.exceptions.RequestException as e:
        return {"status_code":500, "detail": str(e)}