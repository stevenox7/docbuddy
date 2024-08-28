import os
from typing import List, Tuple
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


from backend.core import run_llm


def format_reference_links(references: List[str]) -> str:
    if not references:
        return ""
    ref_string = "References:\n"
    for i, ref in enumerate(sorted(set(references)), 1):
        ref_string += f"{i}. {ref}\n"
    return ref_string


st.title("AI Documentation Assistant")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
    st.session_state.user_inputs = []
    st.session_state.full_conversation = []

user_input = st.text_input("Ask a question:", key="user_query")

if user_input or st.button("Send"):
    with st.spinner("Processing your request..."):
        response_data = run_llm(
            query=user_input,
            conversation_context=st.session_state.full_conversation
        )

        references = [doc.metadata.get("source", "") for doc in response_data.get("context", [])]
        formatted_response = (
            f"{response_data['response']}\n\n{format_reference_links(references)}"
        )

        st.session_state.user_inputs.append(user_input)
        st.session_state.conversation_history.append(formatted_response)
        st.session_state.full_conversation.extend([
            ("user", user_input),
            ("assistant", response_data['response'])
        ])

# Display conversation
for user_msg, ai_msg in zip(
        st.session_state.user_inputs,
        st.session_state.conversation_history
):
    message(user_msg, is_user=True)
    message(ai_msg)