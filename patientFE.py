import streamlit as st
import requests

# Configure the page
st.set_page_config(
    page_title="Patient Portal",
    page_icon="👤"
)

# Custom CSS to reduce padding and font sizes
st.markdown("""
<style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 10rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    .main .block-container {
        max-width: none;
    }
    h1 {
        font-size: 2rem !important;
        margin-bottom: 1rem !important;
    }
    h2 {
        font-size: 1.5rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    h3 {
        font-size: 1.2rem !important;
    }
    .stMarkdown hr {
        margin: 0.5rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# API base URL
API_BASE_URL = "http://localhost:5000"

st.title("👤 Patient Portal")

# Initialize session state for navigation and retention
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_conversation_id' not in st.session_state:
    st.session_state.selected_conversation_id = None
if 'conversations' not in st.session_state:
    st.session_state.conversations = None
if 'current_patient_id' not in st.session_state:
    st.session_state.current_patient_id = None
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = ""

# Navigation functions
def go_to_conversation(conversation_id):
    st.session_state.page = 'conversation'
    st.session_state.selected_conversation_id = conversation_id

def go_back():
    st.session_state.page = 'main'
    st.session_state.selected_conversation_id = None

# Main page
if st.session_state.page == 'main':
    # Patient ID input with session state retention
    patient_id = st.text_input("Patient ID:", placeholder="Enter your patient ID", 
                              value=st.session_state.patient_id, key="patient_id_input")
    st.session_state.patient_id = patient_id

    # Auto-load conversations when patient_id is entered
    if patient_id:
        # Only make API call if patient_id changed or conversations not loaded
        if patient_id != st.session_state.current_patient_id or st.session_state.conversations is None:
            try:
                # Make API call to get conversations
                response = requests.get(f"{API_BASE_URL}/api/patient/conversations/{patient_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data["success"]:
                        st.session_state.conversations = data["data"]
                        st.session_state.current_patient_id = patient_id
                    else:
                        st.error(f"Error: {data.get('error', 'Unknown error')}")
                        st.session_state.conversations = None
                else:
                    st.error(f"API call failed with status code: {response.status_code}")
                    st.session_state.conversations = None
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the server. Make sure the backend is running.")
                st.session_state.conversations = None
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.conversations = None
        
        # Create new conversation form
        st.subheader("Start New Conversation")
        
        with st.form("create_conversation_form"):
            new_conversation_question = st.text_area("Your First Question:", placeholder="Enter your medical question to start a new conversation...")
            new_conversation_image_url = st.text_input("Image URL (optional):", placeholder="Enter image URL if you have a photo to share")
            conversation_submitted = st.form_submit_button("Start New Conversation")
            
            if conversation_submitted and new_conversation_question.strip():
                try:
                    # Prepare data for API call
                    conversation_data = {
                        "patient_id": int(patient_id),
                        "question": new_conversation_question.strip(),
                        "image_url": new_conversation_image_url.strip() if new_conversation_image_url.strip() else None
                    }
                    
                    # Make API call to create conversation
                    create_response = requests.post(
                        f"{API_BASE_URL}/api/patient/conversations",
                        json=conversation_data
                    )
                    
                    if create_response.status_code == 201:
                        response_data = create_response.json()
                        if response_data.get("success") and "conversation_id" in response_data:
                            # Clear conversations cache so it refreshes when we go back
                            st.session_state.conversations = None
                            go_to_conversation(response_data["conversation_id"])
                            st.rerun()
                        else:
                            st.error("Failed to get conversation ID from response.")
                    else:
                        st.error(f"Failed to create conversation. Status code: {create_response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the server. Make sure the backend is running.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            elif conversation_submitted:
                st.error("Please enter a question before starting a new conversation.")
        
        # Display existing conversations from session state
        st.subheader("Your Conversations")
        
        if st.session_state.conversations is not None:
            conversations = st.session_state.conversations
            
            if conversations:
                st.success(f"Found {len(conversations)} conversation(s), scroll down to view.")
                
                # Display each conversation with clickable buttons
                for conv in conversations:
                    with st.expander(f"Conversation {conv['conversation_id']} - Created: {conv['conversation_created_at']}"):
                        if conv['first_query_question']:
                            st.write(f"**First Query:** {conv['first_query_question']}")
                            st.write(f"**Query Date:** {conv['first_query_created_at']}")
                        else:
                            st.write("*No queries in this conversation yet*")
                        
                        # Button to view full conversation
                        if st.button(f"View Full Conversation", key=f"view_{conv['conversation_id']}"):
                            go_to_conversation(conv['conversation_id'])
                            st.rerun()
            else:
                st.info("No conversations found for this patient. Start your first conversation above!")

# Patient conversation page
elif st.session_state.page == 'conversation':
    if st.session_state.selected_conversation_id:
        # Back button
        if st.button("← Back"):
            go_back()
            st.rerun()
        
        st.subheader(f"Conversation {st.session_state.selected_conversation_id}")
        
        try:
            # Make API call to get conversation details
            response = requests.get(f"{API_BASE_URL}/api/clinician/conversation/{st.session_state.selected_conversation_id}")
            
            if response.status_code == 200:
                data = response.json()
                
                if data["success"]:
                    conversation_data = data["data"]
                    
                    if conversation_data:
                        for item in conversation_data:
                            st.write(f"**Query {item['query_id']}:** {item['question']}")
                            st.write(f"**Asked on:** {item['query_created_at']}")
                            
                            if item['response']:
                                st.write(f"**AI Response:** {item['response']}")
                            
                            if item['clinician_response']:
                                st.write(f"**Clinician Response:** {item['clinician_response']}")
                            
                            st.write(f"**Status:** {item['status']}")
                            
                            if item['response_created_at']:
                                st.write(f"**Response Date:** {item['response_created_at']}")
                            
                            st.divider()
                        
                        # Add new query form for patients
                        st.subheader("Add New Query")
                        
                        # Initialize form reset key if not exists
                        if 'form_reset_key' not in st.session_state:
                            st.session_state.form_reset_key = 0
                        
                        with st.form("add_query_form", clear_on_submit=True):
                            new_query_question = st.text_area("Your Question:", placeholder="Enter your medical question...", key=f"query_question_{st.session_state.form_reset_key}")
                            new_query_image_url = st.text_input("Image URL (optional):", placeholder="Enter image URL if you have a photo to share", key=f"query_image_{st.session_state.form_reset_key}")
                            query_submitted = st.form_submit_button("Add Query")
                            
                            if query_submitted and new_query_question.strip():
                                try:
                                    # Prepare data for API call
                                    query_data = {
                                        "question": new_query_question.strip(),
                                        "image_url": new_query_image_url.strip() if new_query_image_url.strip() else None
                                    }
                                    
                                    # Make API call to add query
                                    add_query_response = requests.post(
                                        f"{API_BASE_URL}/api/patient/conversations/{st.session_state.selected_conversation_id}/queries",
                                        json=query_data
                                    )
                                    
                                    if add_query_response.status_code == 201:
                                        st.success("Query added successfully! Refreshing conversation...")
                                        # Increment form reset key to clear form fields
                                        st.session_state.form_reset_key += 1
                                        st.rerun()
                                    else:
                                        st.error(f"Failed to add query. Status code: {add_query_response.status_code}")
                                        
                                except requests.exceptions.ConnectionError:
                                    st.error("Could not connect to the server. Make sure the backend is running.")
                                except Exception as e:
                                    st.error(f"An error occurred: {str(e)}")
                            elif query_submitted:
                                st.error("Please enter a question before adding a query.")
                    else:
                        st.info("No queries found in this conversation.")
                else:
                    st.error(f"Error: {data.get('error', 'Unknown error')}")
            else:
                st.error(f"API call failed with status code: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Make sure the backend is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("No conversation selected.")
        if st.button("← Back"):
            go_back()
            st.rerun()