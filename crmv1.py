import streamlit as st
import pandas as pd

# Initialize an empty DataFrame to hold the customer data
if 'customer_data' not in st.session_state:
    st.session_state['customer_data'] = pd.DataFrame(columns=["Name", "Email", "Phone", "Company"])

# Function to add a new customer
def add_customer(name, email, phone, company):
    new_customer = pd.DataFrame([[name, email, phone, company]], columns=["Name", "Email", "Phone", "Company"])
    st.session_state['customer_data'] = pd.concat([st.session_state['customer_data'], new_customer], ignore_index=True)

# Function to delete a customer
def delete_customer(index):
    st.session_state['customer_data'] = st.session_state['customer_data'].drop(index).reset_index(drop=True)

# Streamlit App Layout
st.title("Basic CRM App")

# Add new customer form
st.header("Add a New Customer")
with st.form("add_customer_form", clear_on_submit=True):
    name = st.text_input("Customer Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    company = st.text_input("Company Name")
    submit_button = st.form_submit_button("Add Customer")
    
    if submit_button and name and email and phone and company:
        add_customer(name, email, phone, company)
        st.success("Customer added successfully!")

# Display the customer data in a table
st.header("Customer List")
if not st.session_state['customer_data'].empty:
    st.dataframe(st.session_state['customer_data'])
else:
    st.write("No customers found.")

# Delete a customer
st.header("Delete a Customer")
delete_index = st.number_input("Enter customer index to delete", min_value=0, max_value=len(st.session_state['customer_data'])-1, step=1)
if st.button("Delete Customer"):
    if delete_index >= 0 and delete_index < len(st.session_state['customer_data']):
        delete_customer(delete_index)
        st.success("Customer deleted successfully!")
    else:
        st.error("Invalid index!")

