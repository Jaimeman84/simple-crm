import streamlit as st
from src.database.db_manager import DatabaseManager
from src.models.prospect import Prospect
from datetime import datetime
import pandas as pd
import time

def main():
    st.set_page_config(page_title="Simple CRM", layout="wide")
    st.title("Simple CRM System")

    # Initialize database
    db = DatabaseManager()

    # Sidebar for navigation
    page = st.sidebar.selectbox("Navigation", ["Dashboard", "Add Prospect", "View Prospects"])

    if page == "Dashboard":
        show_dashboard(db)
    elif page == "Add Prospect":
        show_add_prospect(db)
    elif page == "View Prospects":
        show_view_prospects(db)

def show_dashboard(db):
    st.header("Dashboard")
    prospects = db.get_all_prospects()
    
    # Calculate metrics
    total_prospects = len(prospects)
    status_counts = {}
    for prospect in prospects:
        status_counts[prospect.status] = status_counts.get(prospect.status, 0) + 1

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Prospects", total_prospects)
    with col2:
        st.metric("Active Leads", status_counts.get("Contacted", 0))
    with col3:
        st.metric("Closed Deals", status_counts.get("Closed - Won", 0))

    # Display pipeline breakdown
    st.subheader("Pipeline Breakdown")
    st.bar_chart(status_counts)

def show_add_prospect(db):
    st.header("Add New Prospect")
    
    # Use form to group inputs
    with st.form("add_prospect_form", clear_on_submit=True):
        full_name = st.text_input("Full Name")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email")
        status = st.selectbox(
            "Status",
            ["Cold Lead", "Contacted", "Qualified", "Proposal Sent", 
             "Negotiation", "Closed - Won", "Closed - Lost", "Follow-up Needed"]
        )
        notes = st.text_area("Notes")
        
        submitted = st.form_submit_button("Add Prospect")
        
        if submitted:
            if not all([full_name, phone_number, email]):
                st.error("Please fill in all required fields.")
            else:
                # Check for duplicate email
                if db.check_duplicate_email(email):
                    st.error(f"A prospect with email {email} already exists!")
                else:
                    prospect = Prospect(
                        id=None,
                        full_name=full_name,
                        phone_number=phone_number,
                        email=email,
                        status=status,
                        notes=notes,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.add_prospect(prospect)
                    st.success("Prospect added successfully!")
                    time.sleep(1)  # Give time for success message to be seen
                    st.rerun()  # Refresh the form

def show_view_prospects(db):
    st.header("View Prospects")
    prospects = db.get_all_prospects()
    
    # Convert prospects to a list of dictionaries for the dataframe
    prospects_data = [
        {
            "ID": p.id,
            "Full Name": p.full_name,
            "Phone": p.phone_number,
            "Email": p.email,
            "Status": p.status,
            "Notes": p.notes,
            "Created": p.created_at.strftime("%Y-%m-%d %H:%M") if p.created_at else "",
            "Updated": p.updated_at.strftime("%Y-%m-%d %H:%M") if p.updated_at else "",
        }
        for p in prospects
    ]
    
    if prospects_data:
        # Create a dataframe and display it as a table
        df = pd.DataFrame(prospects_data)
        
        # Add filters at the top
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=sorted(df["Status"].unique()),
                default=[]
            )
        
        with col2:
            search_term = st.text_input("Search by name or email", "")
        
        # Apply filters
        filtered_df = df.copy()
        if status_filter:
            filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df["Full Name"].str.contains(search_term, case=False) |
                filtered_df["Email"].str.contains(search_term, case=False)
            ]
        
        # Display the table with custom styling
        st.dataframe(
            filtered_df,
            use_container_width=True,
            column_config={
                "ID": st.column_config.NumberColumn(
                    "ID",
                    width="small",
                ),
                "Full Name": st.column_config.TextColumn(
                    "Full Name",
                    width="medium"
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    width="small",
                    options=[
                        "Cold Lead",
                        "Contacted",
                        "Qualified",
                        "Proposal Sent",
                        "Negotiation",
                        "Closed - Won",
                        "Closed - Lost",
                        "Follow-up Needed"
                    ]
                ),
                "Notes": st.column_config.TextColumn(
                    "Notes",
                    width="large"
                ),
            },
            hide_index=True,
        )
        
        # Show total number of prospects
        st.info(f"Total Prospects: {len(filtered_df)}")

        # Add delete section below the table
        st.subheader("Delete Prospect")
        
        # Store the delete state in session state
        if 'delete_confirmed' not in st.session_state:
            st.session_state.delete_confirmed = False
        
        # Single column for both dropdown and button
        prospect_to_delete = st.selectbox(
            "Select Prospect to Delete",
            options=[p["ID"] for p in prospects_data],
            format_func=lambda x: f"ID: {x} - {next((p['Full Name'] for p in prospects_data if p['ID'] == x), '')}"
        )
        
        if st.button("Delete Selected Prospect", type="primary", use_container_width=True):
            st.session_state.delete_confirmed = True
            
        # Show confirmation dialog
        if st.session_state.delete_confirmed:
            st.warning(f"Are you sure you want to delete this prospect?")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Yes, Delete"):
                    if db.delete_prospect(prospect_to_delete):
                        st.success("Prospect deleted successfully!")
                        st.session_state.delete_confirmed = False
                        time.sleep(1)  # Give user time to see the success message
                        st.rerun()
                    else:
                        st.error("Failed to delete prospect")
                        st.session_state.delete_confirmed = False
            with col2:
                if st.button("Cancel"):
                    st.session_state.delete_confirmed = False
                    st.rerun()
    else:
        st.info("No prospects found. Add some prospects to see them listed here.")

if __name__ == "__main__":
    main() 