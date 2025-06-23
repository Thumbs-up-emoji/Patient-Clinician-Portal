import streamlit as st
import requests

# Configure the page
st.set_page_config(
    page_title="Clinician Portal",
    page_icon="👨‍⚕️"
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

st.title("👨‍⚕️ Clinician Portal")

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_conversation_id' not in st.session_state:
    st.session_state.selected_conversation_id = None
if 'pending_conversations' not in st.session_state:
    st.session_state.pending_conversations = None
if 'editing_response_id' not in st.session_state:
    st.session_state.editing_response_id = None
if 'edit_text' not in st.session_state:
    st.session_state.edit_text = ""

# Navigation functions
def go_to_review(conversation_id):
    st.session_state.page = 'review'
    st.session_state.selected_conversation_id = conversation_id

def go_back():
    st.session_state.page = 'main'
    st.session_state.selected_conversation_id = None
    st.session_state.editing_response_id = None
    st.session_state.edit_text = ""

def start_editing(response_id, current_text):
    st.session_state.editing_response_id = response_id
    st.session_state.edit_text = current_text

def cancel_editing():
    st.session_state.editing_response_id = None
    st.session_state.edit_text = ""

# Main page
if st.session_state.page == 'main':
    # Auto-load pending conversations
    if st.session_state.pending_conversations is None:
        try:
            # Make API call to get pending conversations
            response = requests.get(f"{API_BASE_URL}/api/clinician/pending-conversations")
            
            if response.status_code == 200:
                data = response.json()
                
                if data["success"]:
                    st.session_state.pending_conversations = data["data"]
                else:
                    st.error(f"Error: {data.get('error', 'Unknown error')}")
                    st.session_state.pending_conversations = []
            else:
                st.error(f"API call failed with status code: {response.status_code}")
                st.session_state.pending_conversations = []
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Make sure the backend is running.")
            st.session_state.pending_conversations = []
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.pending_conversations = []
    
    # Display pending conversations from session state
    if st.session_state.pending_conversations is not None:
        pending_conversations = st.session_state.pending_conversations
        
        if pending_conversations:
            st.subheader("Pending Conversations Requiring Review")
            st.success(f"Found {len(pending_conversations)} conversation(s) with unreviewed responses.")
            
            # Display each pending conversation
            for conv in pending_conversations:
                with st.expander(f"Conversation {conv['conversation_id']} - Created: {conv['conversation_created_at']}"):
                    st.write(f"**Earliest Unreviewed Query:** {conv['earliest_unreviewed_query']}")
                    
                    # Button to view full conversation for clinician review
                    if st.button(f"Review Conversation", key=f"review_{conv['conversation_id']}"):
                        go_to_review(conv['conversation_id'])
                        st.rerun()
        else:
            st.info("No pending conversations requiring review at this time.")

# Clinician review page
elif st.session_state.page == 'review':
    if st.session_state.selected_conversation_id:
        # Back button
        if st.button("← Back"):
            go_back()
            st.rerun()
        
        st.subheader(f"Review Conversation {st.session_state.selected_conversation_id}")
        
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
                                # Check if this response is being edited
                                if st.session_state.editing_response_id == item['response_id']:
                                    st.write("**AI Response (Editing):**")
                                    edited_text = st.text_area(
                                        "Edit Response",
                                        value=st.session_state.edit_text,
                                        height=150,
                                        key=f"edit_area_{item['response_id']}"
                                    )
                                    st.session_state.edit_text = edited_text
                                    
                                    # Save and Cancel buttons
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if st.button(f"Save Changes", key=f"save_{item['response_id']}"):
                                            try:
                                                update_response = requests.put(
                                                    f"{API_BASE_URL}/api/clinician/responses/edit/{item['response_id']}",
                                                    json={"clinician_response": edited_text}
                                                )
                                                
                                                if update_response.status_code == 200:
                                                    st.success("Response updated successfully!")
                                                    cancel_editing()
                                                    # Clear pending conversations to refresh on back
                                                    st.session_state.pending_conversations = None
                                                    st.rerun()
                                                else:
                                                    st.error("Failed to update response")
                                            except Exception as e:
                                                st.error(f"Error updating response: {str(e)}")
                                    
                                    with col2:
                                        if st.button(f"Cancel", key=f"cancel_{item['response_id']}"):
                                            cancel_editing()
                                            st.rerun()
                                else:
                                    # Display normal AI response
                                    st.write(f"**AI Response:** {item['response']}")
                            
                            if item['clinician_response']:
                                st.write(f"**Clinician Response:** {item['clinician_response']}")
                            
                            st.write(f"**Status:** {item['status']}")
                            
                            if item['response_created_at']:
                                st.write(f"**Response Date:** {item['response_created_at']}")
                            
                            # Add verify and edit buttons for unreviewed responses
                            if item['status'] == 'unreviewed' and item['response_id'] and st.session_state.editing_response_id != item['response_id']:
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    if st.button(f"Verify Response", key=f"verify_{item['response_id']}"):
                                        try:
                                            verify_response = requests.put(f"{API_BASE_URL}/api/clinician/responses/verify/{item['response_id']}")
                                            
                                            if verify_response.status_code == 200:
                                                st.success("Response verified successfully!")
                                                # Clear pending conversations to refresh on back
                                                st.session_state.pending_conversations = None
                                                st.rerun()
                                            else:
                                                st.error("Failed to verify response")
                                        except Exception as e:
                                            st.error(f"Error verifying response: {str(e)}")
                                
                                with col2:
                                    if st.button(f"Edit Response", key=f"edit_{item['response_id']}"):
                                        start_editing(item['response_id'], item['response'] or "")
                                        st.rerun()
                            
                            st.divider()
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