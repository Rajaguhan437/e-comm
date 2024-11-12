import streamlit as st, time

from api.loginAPI import login_api, signup_api

button_style = """
    <style>
    div.stButton > button {
        margin-left: 43%;
    }
    div.stButton > button:hover {
        color: #28a745;
        border-color: #28a745;
    }
    div.stButton > button:focus {
        background-color: #28a745;
        color: white;
    }
    div.stButton > button:focus:not(:active) {
        color: #fff;
        border-color: #28a745;
    }
    .stApp [data-testid="stToolbar"] {
        display: none;
    }
    </style>
"""


def app():
    st.title('Welcome to :orange[QuickCart] 🛍️')

    choice = st.selectbox('Login / SignUp', ["Login", "Sign Up"])
    if choice == 'Login':
        username = st.text_input('UserName', placeholder="Enter Your NickName")
        password = st.text_input('Password', type='password', placeholder="Enter Your Password")

        st.write('')
        st.markdown(button_style, unsafe_allow_html=True)
        
        if st.button("Login", key='Login'):
            st.write('')

            with st.spinner("Logging you In"):
                time.sleep(2)
            
            message = login_api(username, password)
            if message['status_code'] == 500:
                st.error(message['detail'])
            else:
                st.session_state.logged_in = True
                st.success("Login Success!", icon="✅")
                
                time.sleep(2)

    else:
        username = st.text_input('UserName', placeholder="Enter Your NickName")
        email = st.text_input('Email Address', placeholder="Enter Your Email Address")
        password = st.text_input('Password', type='password', placeholder="Enter Your Password")
        confirm_password = st.text_input('Confirm Password', type='password', placeholder='Confirm Your Password')

        if username and email and password and confirm_password:
            if password != confirm_password:
                st.warning("Passwords do not match. Please try again.")
                return

        role = "Admin" if "admin" in email else "Customer"
        
        st.write('')
        st.markdown(button_style, unsafe_allow_html=True)
        
        if st.button("Create my Account", key='Create my Account'):
            st.write('')
            
            message = signup_api(username, email, password, role)
            if message['status_code'] == 500:
                st.error(message['detail'])
            else:
                with st.spinner("Processing..."):
                    time.sleep(2)
                
                st.success("Account created successfully!", icon="✅")
                st.balloons()
                # st.rerun()

if __name__ == "__main__":
    app()
