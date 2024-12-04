Explanation: CRMv1

    Customer Data Management: The app uses a DataFrame from pandas to hold customer information. It's stored in the st.session_state to persist across app reruns.
    Adding Customers: Users can input customer details such as name, email, phone, and company into a form, and the data is added to the DataFrame.
    Viewing Customers: The customer list is displayed using st.dataframe(), showing all the customers added so far.
    Deleting Customers: Users can input the index of the customer they want to delete, and once the button is pressed, the corresponding customer is removed.

Explanation: CRMv1 + Contact Management

Track contacts for each customer: Each customer will have a list of contacts.
Add contacts: Users can add contacts to a specific customer.
View contacts: Each customer will have an associated contact list.
Delete contacts: Users can delete a contact for a specific customer.




    


    
