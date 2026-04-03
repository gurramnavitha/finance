import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Finance Dashboard", layout="wide")

if "token" not in st.session_state:
    st.session_state["token"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "user_data" not in st.session_state:
    st.session_state["user_data"] = None

def login(email, password):
    response = requests.post(f"{API_URL}/auth/login", data={"username": email, "password": password})
    if response.status_code == 200:
        st.session_state["token"] = response.json().get("access_token")
        
        # Fetch user details
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        user_response = requests.get(f"{API_URL}/users/me", headers=headers)
        if user_response.status_code == 200:
            user_data = user_response.json()
            st.session_state["user_data"] = user_data
            st.session_state["role"] = user_data.get("role")
        st.rerun()
    else:
        st.error("Invalid credentials!")

def logout():
    st.session_state["token"] = None
    st.session_state["role"] = None
    st.session_state["user_data"] = None
    st.rerun()

# --- Unauthenticated View ---
if not st.session_state["token"]:
    st.title("Finance Processing System - Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            login(email, password)

# --- Authenticated View ---
else:
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    st.sidebar.title(f"Welcome, {st.session_state['user_data']['name']}")
    st.sidebar.write(f"Role: **{st.session_state['role']}**")
    if st.sidebar.button("Logout"):
        logout()

    page = st.sidebar.radio("Navigation", ["Dashboard", "Records", "Admin Panel"])

    if page == "Dashboard":
        st.title("Dashboard")
        
        # Summary
        summary_resp = requests.get(f"{API_URL}/dashboard/summary", headers=headers)
        if summary_resp.status_code == 200:
            summary = summary_resp.json()
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"${summary['total_income']:,.2f}")
            col2.metric("Total Expenses", f"${summary['total_expenses']:,.2f}")
            col3.metric("Net Balance", f"${summary['net_balance']:,.2f}")
        else:
            st.error("Failed to load dashboard data.")

        # Category Breakdown
        st.subheader("Category Summaries")
        colA, colB = st.columns(2)
        with colA:
            st.write("Income by Category")
            inc_cat = requests.get(f"{API_URL}/dashboard/category/income", headers=headers)
            if inc_cat.status_code == 200 and inc_cat.json():
                st.dataframe(pd.DataFrame(inc_cat.json()))
            else:
                st.write("No data")
        
        with colB:
            st.write("Expenses by Category")
            exp_cat = requests.get(f"{API_URL}/dashboard/category/expense", headers=headers)
            if exp_cat.status_code == 200 and exp_cat.json():
                st.dataframe(pd.DataFrame(exp_cat.json()))
            else:
                st.write("No data")

    elif page == "Records":
        st.title("Financial Records")
        if st.session_state["role"] in ["Admin", "Analyst"]:
            records_resp = requests.get(f"{API_URL}/records/", headers=headers)
            if records_resp.status_code == 200:
                df = pd.DataFrame(records_resp.json())
                if not df.empty:
                    st.dataframe(df)
                else:
                    st.info("No records found.")
            else:
                st.error("Failed to fetch records.")
        else:
            st.warning("Viewers do not have access to raw records.")

    elif page == "Admin Panel":
        st.title("Admin Panel")
        if st.session_state["role"] == "Admin":
            tab1, tab2 = st.tabs(["Add Record", "Create User"])
            
            with tab1:
                st.subheader("Create a New Financial Record")
                with st.form("record_form"):
                    amount = st.number_input("Amount", min_value=0.01)
                    type_val = st.selectbox("Type", ["income", "expense"])
                    category = st.text_input("Category")
                    description = st.text_area("Description")
                    submitted = st.form_submit_button("Add Record")
                    
                    if submitted:
                        payload = {
                            "amount": amount,
                            "type": type_val,
                            "category": category,
                            "description": description
                        }
                        res = requests.post(f"{API_URL}/records/", json=payload, headers=headers)
                        if res.status_code == 200:
                            st.success("Record added successfully!")
                        else:
                            st.error("Failed to add record.")

            with tab2:
                st.subheader("Create a New User")
                with st.form("user_form"):
                    u_name = st.text_input("Name")
                    u_email = st.text_input("Email")
                    u_pwd = st.text_input("Password", type="password")
                    u_role = st.selectbox("Role", ["Admin", "Analyst", "Viewer"])
                    submitted_user = st.form_submit_button("Create User")
                    
                    if submitted_user:
                        payload = {
                            "name": u_name,
                            "email": u_email,
                            "password": u_pwd,
                            "role": u_role
                        }
                        res = requests.post(f"{API_URL}/users/", json=payload, headers=headers)
                        if res.status_code == 200:
                            st.success("User created successfully!")
                        else:
                            st.error(f"Failed to create user. {res.text}")
        else:
            st.error("Access Denied: Admins Only")
