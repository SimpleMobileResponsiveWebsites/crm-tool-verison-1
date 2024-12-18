Explanation: CRMv1 - crmv1.py

    Customer Data Management: The app uses a DataFrame from pandas to hold customer information. It's stored in the st.session_state to persist across app reruns.
    Adding Customers: Users can input customer details such as name, email, phone, and company into a form, and the data is added to the DataFrame.
    Viewing Customers: The customer list is displayed using st.dataframe(), showing all the customers added so far.
    Deleting Customers: Users can input the index of the customer they want to delete, and once the button is pressed, the corresponding customer is removed.

Explanation: CRMv1 + Contact Management crmv2.py

Track contacts for each customer: Each customer will have a list of contacts.
Add contacts: Users can add contacts to a specific customer.
View contacts: Each customer will have an associated contact list.
Delete contacts: Users can delete a contact for a specific customer.

Explanation:  CRMv1 + Sales Management, crmv3.py

Key Changes:

    Sales Management:
        Add Sales Deal: Users can now add sales deals associated with a customer. The deal includes details like deal name, stage, value, and close date.
        Delete Sales Deal: Users can delete sales deals associated with a customer.
        View Sales Deals: Displays the sales deals for a selected customer in a table format.

    sales_data: A new dictionary sales_data stores sales deals, where the key is the customer's name and the value is a DataFrame containing the deal details.

How It Works:

    Customer Management: You can add, delete, and view customers as before.
    Sales Management:
        After selecting a customer from the dropdown, you can add sales deals (e.g., "Prospecting", "Negotiation", etc.).
        Sales deals for the selected customer are displayed in a table format.
        Sales deals can be deleted by selecting an index from the sales deal list.


Explanation:  CRMv1 + Sales Pipeline Managment, crmv4.py

Key Changes:

    Sales Pipeline Management:
        Add Opportunity: Users can add sales opportunities (or deals) to a customer’s pipeline with details like opportunity name, stage, value, and close date.
        Move Opportunity Through Stages: Users can update the stage of an opportunity (e.g., move it from "Lead" to "Qualified").
        Delete Opportunity: Users can delete an opportunity for a selected customer.
        View Opportunities: All opportunities for a selected customer are displayed in a table.

    pipeline_data: A dictionary pipeline_data is added to store the sales pipeline for each customer. The key is the customer's name, and the value is a DataFrame containing the opportunity details.

How It Works:

    Customer Management: You can continue to add, view, and delete customers.
    Pipeline Management:
        After selecting a customer, you can add new opportunities to the customer's pipeline.
        You can move opportunities between different stages of the sales process.
        You can view and delete opportunities in the pipeline.



    


    
