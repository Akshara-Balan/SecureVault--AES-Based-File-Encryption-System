import streamlit as st
import json
import os

USER_DB = "users.json"

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

def create_account():
    st.subheader("Create Account")
    username = st.text_input("Choose a Username:")
    password = st.text_input("Choose a Password:", type="password")

    if st.button("Register"):
        users = load_users()
        if username in users:
            st.error("❌ Username already exists! Try logging in.")
        else:
            users[username] = {"password": password, "files": []}
            save_users(users)
            st.success("✅ Account created! Now you can log in.")

def user_login():
    st.subheader("Login")
    username = st.text_input("Enter your Username:")
    password = st.text_input("Enter your Password:", type="password")

    if st.button("Login"):
        users = load_users()
        if username in users and users[username]["password"] == password:
            st.success(f"✅ Welcome, {username}!")
            return username
        else:
            st.error("❌ Invalid credentials.")
