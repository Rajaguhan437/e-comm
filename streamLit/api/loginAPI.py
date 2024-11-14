import requests

from api.cookieTokenManager import url, get_tokens, cookie_manager


def signup_api(username, email, password, role):
    url_ = url + "user/signup/"
    data = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }
    try:
        response = requests.post(url_, json=data)
            
        if response.status_code != 200:
            return f"Error: {response.content.decode()}"
    
    except Exception as e:
        return f"Error: {str(e)}"


def login_api(username, password):
    url_ = url + "user/login/"
    data = {
        "username": username,
        "password": password,
    }
    
    try:
        response = requests.post(url_, json=data)
        if response.status_code != 200:
            return f"Error: {response.content.decode()}"
        
        tokens = response.json()

        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")

        access_token = tokens['Response']['raw_headers'][0][1][13:-22]
        refresh_token = tokens['Response']['raw_headers'][1][1][14:-22]

        cookie_manager.set(cookie="access_token", val=access_token, key="access")#, expires_at=3600)  # 1 hour
        cookie_manager.set(cookie="refresh_token", val=refresh_token, key="refresh")#, key="tokens")#, expires_at=7*24*3600)  # 7 days

        return {"status_code":200, "detail":"Log In Successful"}

    except requests.exceptions.RequestException as e:
        return {"status_code":500, "detail": str(e)}
    

