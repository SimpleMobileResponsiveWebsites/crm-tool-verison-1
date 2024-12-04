import streamlit as st
import pandas as pd

# Initialize an empty DataFrame to hold the customer data and sales pipeline data
if 'customer_data' not in st.session_state:
    st.session_state['customer_data'] = pd.DataFrame(columns=["Name", "Email", "Phone", "Company"])

if 'pipeline_data' not in st.session_state:
    st.session_state['pipeline_data'] = {}

# Function to add a new customer
def add_customer(name, email, phone, company):
    new_customer = pd.DataFrame([[name, email, phone, company]], columns=["Name", "Email", "Phone", "Company"])
    st.session_state['customer_data'] = pd.concat([st.session_state['customer_data'], new_customer], ignore_index=True)

# Function to delete a customer
def delete_customer(index):
    st.session_state['customer_data'] = st.session_state['customer_data'].drop(index).reset_index(drop=True)
    customer_name = st.session_state['customer_data'].iloc[index]["Name"]
    # Also delete associated pipeline data
    if customer_name in st.session_state['pipeline_data']:
        del st.session_state['pipeline_data'][customer_name]

# Function to add an opportunity (sales pipeline) for a customer
def add_opportunity(customer_name, opportunity_name, stage, value, close_date):
    if customer_name not in st.session_state['pipeline_data']:
        st.session_state['pipeline_data'][customer_name] = pd.DataFrame(columns=["Opportunity Name", "Stage", "Value", "Close Date"])
    
    new_opportunity = pd.DataFrame([[opportunity_name, stage, value, close_date]], columns=["Opportunity Name", "Stage", "Value", "Close Date"])
    st.session_state['pipeline_data'][customer_name] = pd.concat([st.session_state['pipeline_data'][customer_name], new_opportunity], ignore_index=True)

# Function to move an opportunity to a new stage
def update_opportunity_stage(customer_name, index, new_stage):
    if customer_name in st.session_state['pipeline_data']:
        st.session_state['pipeline_data'][customer_name].at[index, 'Stage'] = new_stage

# Function to delete an opportunity for a customer
def delete_opportunity(customer_name, index):
    if customer_name in st.session_state['pipeline_data']:
        st.session_state['pipeline_data'][customer_name] = st.session_state['pipeline_data'][customer_name].drop(index).reset_index(drop=True)

# Streamlit App Layout
st.title("Basic CRM App with Pipeline Management")

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

# Sales Pipeline Management section
st.header("Manage Sales Pipeline for a Customer")
customer_names = st.session_state['customer_data']['Name'].tolist()
selected_customer = st.selectbox("Select a Customer", customer_names)

# Add new opportunity form (pipeline management)
with st.form("add_opportunity_form", clear_on_submit=True):
    if selected_customer:
        opportunity_name = st.text_input("Opportunity Name")
        opportunity_stage = st.selectbox("Stage", ["Lead", "Qualified", "Proposal Sent", "Negotiation", "Closed Won", "Closed Lost"])
        opportunity_value = st.number_input("Opportunity Value", min_value=0.0, step=0.1)
        close_date = st.date_input("Close Date")
        opportunity_submit_button = st.form_submit_button("Add Opportunity")
        
        if opportunity_submit_button and opportunity_name and opportunity_stage and opportunity_value and close_date:
            add_opportunity(selected_customer, opportunity_name, opportunity_stage, opportunity_value, close_date)
            st.success("Opportunity added successfully!")

# Display opportunities (sales pipeline) for the selected customer
if selected_customer in st.session_state['pipeline_data'] and not st.session_state['pipeline_data'][selected_customer].empty:
    st.subheader(f"Sales Pipeline for {selected_customer}")
    st.dataframe(st.session_state['pipeline_data'][selected_customer])
else:
    st.write("No opportunities found for this customer.")

# Move an opportunity to a new stage
if selected_customer in st.session_state['pipeline_data']:
    if not st.session_state['pipeline_data'][selected_customer].empty:
        opportunity_index = st.number_input("Enter opportunity index to move", min_value=0, max_value=len(st.session_state['pipeline_data'][selected_customer])-1, step=1)
        new_stage = st.selectbox("Select new stage for opportunity", ["Lead", "Qualified", "Proposal Sent", "Negotiation", "Closed Won", "Closed Lost"])
        if st.button("Move Opportunity to New Stage"):
            if opportunity_index >= 0 and opportunity_index < len(st.session_state['pipeline_data'][selected_customer]):
                update_opportunity_stage(selected_customer, opportunity_index, new_stage)
                st.success("Opportunity stage updated successfully!")
            else:
                st.error("Invalid opportunity index!")

# Delete an opportunity for the selected customer
if selected_customer in st.session_state['pipeline_data']:
    if not st.session_state['pipeline_data'][selected_customer].empty:
        opportunity_delete_index = st.number_input("Enter opportunity index to delete", min_value=0, max_value=len(st.session_state['pipeline_data'][selected_customer])-1, step=1)
        if st.button("Delete Opportunity"):
            if opportunity_delete_index >= 0 and opportunity_delete_index < len(st.session_state['pipeline_data'][selected_customer]):
                delete_opportunity(selected_customer, opportunity_delete_index)
                st.success("Opportunity deleted successfully!")
            else:
                st.error("Invalid opportunity index!")
