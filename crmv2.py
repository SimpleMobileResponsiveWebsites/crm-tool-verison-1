import streamlit as st
import pandas as pd

# Initialize empty DataFrames to hold the customer and contact data
if 'customer_data' not in st.session_state:
    st.session_state['customer_data'] = pd.DataFrame(columns=["Name", "Email", "Phone", "Company"])

if 'contact_data' not in st.session_state:
    st.session_state['contact_data'] = {}

# Function to add a new customer
def add_customer(name, email, phone, company):
    new_customer = pd.DataFrame([[name, email, phone, company]], columns=["Name", "Email", "Phone", "Company"])
    st.session_state['customer_data'] = pd.concat([st.session_state['customer_data'], new_customer], ignore_index=True)

# Function to delete a customer
def delete_customer(index):
    st.session_state['customer_data'] = st.session_state['customer_data'].drop(index).reset_index(drop=True)
    customer_name = st.session_state['customer_data'].iloc[index]["Name"]
    # Also delete associated contacts
    if customer_name in st.session_state['contact_data']:
        del st.session_state['contact_data'][customer_name]

# Function to add a contact for a specific customer
def add_contact(customer_name, contact_name, contact_email, contact_phone, contact_role):
    if customer_name not in st.session_state['contact_data']:
        st.session_state['contact_data'][customer_name] = pd.DataFrame(columns=["Contact Name", "Email", "Phone", "Role"])
    
    new_contact = pd.DataFrame([[contact_name, contact_email, contact_phone, contact_role]], columns=["Contact Name", "Email", "Phone", "Role"])
    st.session_state['contact_data'][customer_name] = pd.concat([st.session_state['contact_data'][customer_name], new_contact], ignore_index=True)

# Function to delete a contact for a specific customer
def delete_contact(customer_name, index):
    if customer_name in st.session_state['contact_data']:
        st.session_state['contact_data'][customer_name] = st.session_state['contact_data'][customer_name].drop(index).reset_index(drop=True)

# Streamlit App Layout
st.title("Basic CRM App with Contact Management")

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

# Contact management section
st.header("Manage Contacts for a Customer")
customer_names = st.session_state['customer_data']['Name'].tolist()
selected_customer = st.selectbox("Select a Customer", customer_names)

# Add new contact form
with st.form("add_contact_form", clear_on_submit=True):
    if selected_customer:
        contact_name = st.text_input("Contact Name")
        contact_email = st.text_input("Contact Email")
        contact_phone = st.text_input("Contact Phone")
        contact_role = st.text_input("Contact Role (e.g., Sales Rep, Support)")
        contact_submit_button = st.form_submit_button("Add Contact")
        
        if contact_submit_button and contact_name and contact_email and contact_phone and contact_role:
            add_contact(selected_customer, contact_name, contact_email, contact_phone, contact_role)
            st.success("Contact added successfully!")

# Display contacts for the selected customer
if selected_customer in st.session_state['contact_data'] and not st.session_state['contact_data'][selected_customer].empty:
    st.subheader(f"Contacts for {selected_customer}")
    st.dataframe(st.session_state['contact_data'][selected_customer])
else:
    st.write("No contacts found for this customer.")

# Delete a contact for the selected customer
if selected_customer in st.session_state['contact_data']:
    if not st.session_state['contact_data'][selected_customer].empty:
        contact_delete_index = st.number_input("Enter contact index to delete", min_value=0, max_value=len(st.session_state['contact_data'][selected_customer])-1, step=1)
        if st.button("Delete Contact"):
            if contact_delete_index >= 0 and contact_delete_index < len(st.session_state['contact_data'][selected_customer]):
                delete_contact(selected_customer, contact_delete_index)
                st.success("Contact deleted successfully!")
            else:
                st.error("Invalid index!")
