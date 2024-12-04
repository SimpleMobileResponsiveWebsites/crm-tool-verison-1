import streamlit as st
import pandas as pd

# Initialize an empty DataFrame to hold the customer data and sales deals
if 'customer_data' not in st.session_state:
    st.session_state['customer_data'] = pd.DataFrame(columns=["Name", "Email", "Phone", "Company"])

if 'sales_data' not in st.session_state:
    st.session_state['sales_data'] = {}

# Function to add a new customer
def add_customer(name, email, phone, company):
    new_customer = pd.DataFrame([[name, email, phone, company]], columns=["Name", "Email", "Phone", "Company"])
    st.session_state['customer_data'] = pd.concat([st.session_state['customer_data'], new_customer], ignore_index=True)

# Function to delete a customer
def delete_customer(index):
    st.session_state['customer_data'] = st.session_state['customer_data'].drop(index).reset_index(drop=True)
    customer_name = st.session_state['customer_data'].iloc[index]["Name"]
    # Also delete associated sales data
    if customer_name in st.session_state['sales_data']:
        del st.session_state['sales_data'][customer_name]

# Function to add a sales deal for a specific customer
def add_sales_deal(customer_name, deal_name, stage, value, close_date):
    if customer_name not in st.session_state['sales_data']:
        st.session_state['sales_data'][customer_name] = pd.DataFrame(columns=["Deal Name", "Stage", "Value", "Close Date"])
    
    new_deal = pd.DataFrame([[deal_name, stage, value, close_date]], columns=["Deal Name", "Stage", "Value", "Close Date"])
    st.session_state['sales_data'][customer_name] = pd.concat([st.session_state['sales_data'][customer_name], new_deal], ignore_index=True)

# Function to delete a sales deal for a specific customer
def delete_sales_deal(customer_name, index):
    if customer_name in st.session_state['sales_data']:
        st.session_state['sales_data'][customer_name] = st.session_state['sales_data'][customer_name].drop(index).reset_index(drop=True)

# Streamlit App Layout
st.title("Basic CRM App with Sales Management")

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

# Sales Management section
st.header("Manage Sales Deals for a Customer")
customer_names = st.session_state['customer_data']['Name'].tolist()
selected_customer = st.selectbox("Select a Customer", customer_names)

# Add new sales deal form
with st.form("add_sales_deal_form", clear_on_submit=True):
    if selected_customer:
        deal_name = st.text_input("Deal Name")
        deal_stage = st.selectbox("Deal Stage", ["Prospecting", "Negotiation", "Closed Won", "Closed Lost"])
        deal_value = st.number_input("Deal Value", min_value=0.0, step=0.1)
        close_date = st.date_input("Close Date")
        deal_submit_button = st.form_submit_button("Add Sales Deal")
        
        if deal_submit_button and deal_name and deal_stage and deal_value and close_date:
            add_sales_deal(selected_customer, deal_name, deal_stage, deal_value, close_date)
            st.success("Sales deal added successfully!")

# Display sales deals for the selected customer
if selected_customer in st.session_state['sales_data'] and not st.session_state['sales_data'][selected_customer].empty:
    st.subheader(f"Sales Deals for {selected_customer}")
    st.dataframe(st.session_state['sales_data'][selected_customer])
else:
    st.write("No sales deals found for this customer.")

# Delete a sales deal for the selected customer
if selected_customer in st.session_state['sales_data']:
    if not st.session_state['sales_data'][selected_customer].empty:
        deal_delete_index = st.number_input("Enter sales deal index to delete", min_value=0, max_value=len(st.session_state['sales_data'][selected_customer])-1, step=1)
        if st.button("Delete Sales Deal"):
            if deal_delete_index >= 0 and deal_delete_index < len(st.session_state['sales_data'][selected_customer]):
                delete_sales_deal(selected_customer, deal_delete_index)
                st.success("Sales deal deleted successfully!")
            else:
                st.error("Invalid index!")
