import streamlit as st
import requests
import extra_streamlit_components as stx
import uuid

url = "http://127.0.0.1:8000/"

cookie_manager = stx.CookieManager(key="key"+str(uuid.uuid1()))

def get_tokens():
    cookie_data = cookie_manager.get_all()
    
    return {
        "access_token": cookie_data.get("access_token"),
        "refresh_token": cookie_data.get("refresh_token")
    }

def is_logged_in():
    tokens = get_tokens()
    return bool(tokens.get("access_token"))

def del_access_token():
    pass
def del_refresh_token():
    pass

def logout():
    st.session_state.logged_in = False
    #del_access_token()
    #del_refresh_token()  ## second token not getting deleted
    unique_id = str(uuid.uuid4())  # Generate a unique identifier for each logout
    cookie_manager.delete("access_token", key=f"del_access_token_{unique_id}")
    cookie_manager.delete("refresh_token", key=f"del_refresh_token_{unique_id}")

def refresh_access_token():

    refresh_token = cookie_manager.get("refresh_token")
    
    logout()
    if not refresh_token:
        return False
        
    refresh_url = url + "user/refresh/refresh?refresh_token="+refresh_token
    refresh_url = url + "user/refresh/"

    try:
        response = requests.post(
            refresh_url,
            json={"refresh_token": refresh_token}
        )
        
        if response.status_code == 200:
            new_tokens = response.json()

            access_token = new_tokens.get("access_token")
            refresh_token = new_tokens.get("refresh_token")

            cookie_manager.set(cookie="access_token", val=access_token, key="access")#, expires_at=3600)  # 1 hour
            cookie_manager.set(cookie="refresh_token", val=refresh_token, key="refresh")#, key="tokens")#, expires_at=7*24*3600)  # 7 days

            return True
    except requests.exceptions.RequestException as e:
        return {"status_code":500, "detail": str(e)}
    
    return False
