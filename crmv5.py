import streamlit as st
import pandas as pd

# Initialize the session state to hold customer data and sales pipeline data
if 'customer_data' not in st.session_state:
    st.session_state['customer_data'] = pd.DataFrame(columns=["Name", "Email", "Phone", "Company"])

if 'pipeline_data' not in st.session_state:
    st.session_state['pipeline_data'] = {}

# Function to add a new customer
def add_customer(name, email, phone, company):
    new_customer = pd.DataFrame([[name, email, phone, company]], columns=["Name", "Email", "Phone", "Company"])
    st.session_state['customer_data'] = pd.concat([st.session_state['customer_data'], new_customer], ignore_index=True)

# Function to add an opportunity (sales pipeline) for a customer
def add_opportunity(customer_name, opportunity_name, stage, value, close_date):
    if customer_name not in st.session_state['pipeline_data']:
        st.session_state['pipeline_data'][customer_name] = pd.DataFrame(columns=["Opportunity Name", "Stage", "Value", "Close Date"])
    
    new_opportunity = pd.DataFrame([[opportunity_name, stage, value, close_date]], columns=["Opportunity Name", "Stage", "Value", "Close Date"])
    st.session_state['pipeline_data'][customer_name] = pd.concat([st.session_state['pipeline_data'][customer_name], new_opportunity], ignore_index=True)

# Reporting Tool Section
st.title("CRM Reporting Tool")

# Customer Report Section
st.header("Customer Report")
if not st.session_state['customer_data'].empty:
    total_customers = len(st.session_state['customer_data'])
    st.write(f"Total Customers: {total_customers}")
    st.dataframe(st.session_state['customer_data'])
else:
    st.write("No customer data available.")

# Sales Pipeline Report Section
st.header("Sales Pipeline Report")
if st.session_state['pipeline_data']:
    # Create a DataFrame to summarize pipeline data
    pipeline_summary = []
    for customer, opportunities in st.session_state['pipeline_data'].items():
        for index, row in opportunities.iterrows():
            pipeline_summary.append({
                "Customer": customer,
                "Opportunity Name": row["Opportunity Name"],
                "Stage": row["Stage"],
                "Value": row["Value"],
                "Close Date": row["Close Date"]
            })
    
    if pipeline_summary:
        pipeline_df = pd.DataFrame(pipeline_summary)
        st.dataframe(pipeline_df)
    else:
        st.write("No opportunities found.")

    # Calculate total value of opportunities by stage
    stage_summary = pipeline_df.groupby('Stage').agg({'Value': 'sum'}).reset_index()
    st.subheader("Total Opportunity Value by Stage")
    st.dataframe(stage_summary)

# Customer with Most Opportunities
st.header("Top Customers by Opportunities")
customer_opportunities_count = {customer: len(opportunities) for customer, opportunities in st.session_state['pipeline_data'].items()}
top_customers = sorted(customer_opportunities_count.items(), key=lambda x: x[1], reverse=True)

if top_customers:
    st.write("Top Customers with Most Opportunities:")
    for customer, count in top_customers:
        st.write(f"{customer}: {count} opportunities")
else:
    st.write("No opportunities available.")

# Total Value of Opportunities Report
st.header("Total Value of All Opportunities")
total_pipeline_value = sum([opportunity["Value"].sum() for opportunities in st.session_state['pipeline_data'].values() for opportunity in [opportunities]])
st.write(f"Total value of all opportunities: ${total_pipeline_value:,.2f}")

# Streamlit Form to add customers and opportunities (optional)
st.sidebar.header("Add New Data")
with st.sidebar.form("add_customer_form", clear_on_submit=True):
    name = st.text_input("Customer Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    company = st.text_input("Company Name")
    submit_button = st.form_submit_button("Add Customer")
    
    if submit_button and name and email and phone and company:
        add_customer(name, email, phone, company)
        st.sidebar.success("Customer added successfully!")

with st.sidebar.form("add_opportunity_form", clear_on_submit=True):
    selected_customer = st.selectbox("Select a Customer for Opportunity", st.session_state['customer_data']['Name'].tolist())
    opportunity_name = st.text_input("Opportunity Name")
    stage = st.selectbox("Stage", ["Lead", "Qualified", "Proposal Sent", "Negotiation", "Closed Won", "Closed Lost"])
    value = st.number_input("Opportunity Value", min_value=0.0, step=0.1)
    close_date = st.date_input("Close Date")
    opportunity_submit_button = st.form_submit_button("Add Opportunity")
    
    if opportunity_submit_button and opportunity_name and stage and value and close_date:
        add_opportunity(selected_customer, opportunity_name, stage, value, close_date)
        st.sidebar.success("Opportunity added successfully!")
