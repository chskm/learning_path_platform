# frontend/main.py
import streamlit as st
import requests
import json

# Backend URL (set by Elastic Beanstalk)
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")

st.title("Learning Path Platform")

# Session state for authentication
if "token" not in st.session_state:
    st.session_state.token = None

# Register/Login UI
if not st.session_state.token:
    tab1, tab2 = st.tabs(["Register", "Login"])
    
    with tab1:
        st.header("Register")
        name = st.text_input("Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        background = st.selectbox("Background", ["Computer Science", "Civil Engineering", "Electronics"], key="reg_background")
        if st.button("Register"):
            response = requests.post(f"{BACKEND_URL}/register", json={
                "name": name,
                "email": email,
                "password": password,
                "background": background
            })
            if response.status_code == 200:
                st.success("Registration successful! Please login.")
            else:
                st.error(response.json().get("detail", "Registration failed"))

    with tab2:
        st.header("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            response = requests.post(f"{BACKEND_URL}/login", json={
                "email": email,
                "password": password
            })
            if response.status_code == 200:
                st.session_state.token = response.json()["token"]
                st.success("Login successful!")
            else:
                st.error(response.json().get("detail", "Login failed"))
else:
    st.header("Submit Your Goal")
    goal = st.text_input("Career Goal (e.g., Python Developer)")
    experience = st.selectbox("Experience", ["Beginner", "Intermediate", "Advanced"])
    if st.button("Get Learning Path"):
        response = requests.post(
            f"{BACKEND_URL}/goals",
            json={"goal": goal, "experience": experience},
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        if response.status_code == 200:
            learning_path = response.json()["learning_path"]
            st.success(f"Your Learning Path: {learning_path}")
        else:
            st.error(response.json().get("detail", "Failed to get learning path"))
    if st.button("Logout"):
        st.session_state.token = None
        st.experimental_rerun()