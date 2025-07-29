import os
import google.generativeai as genai
import requests
import json
import streamlit as st
from dotenv import load_dotenv

# Import protos for direct object creation (essential for robust tool handling)
import google.generativeai.protos as genai_protos

# --- Load environment variables FIRST ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Rashmeet's MCP(Model Context Protocol)", page_icon="📝", layout="centered")

# Custom CSS for a better look and feel, including chat bubbles
st.markdown(
    """
    <style>
    /* Main container styling for padding and max width */
    .reportview-container .main .block-container {
        max-width: 700px;
        padding-top: 2rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 5rem; /* Increased padding to account for fixed input */
    }
    /* Button styling for a more interactive feel */
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        font-size: 1.1rem;
        background-color: #4CAF50; /* A pleasant green */
        color: white;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px); /* Slight lift on hover */
    }
    .stButton>button:active {
        background-color: #3e8e41;
        transform: translateY(0); /* Press effect */
    }
    /* Text input styling */
    .stTextInput>div>div>input {
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
    }
    /* Custom chat bubble styles */
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 8px;
        max-width: 80%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        font-size: 0.95rem;
    }
    .user-message {
        background-color: #e0f2f7; /* Light blue */
        margin-left: auto; /* Aligns to the right */
        text-align: right;
        border-bottom-right-radius: 2px; /* Slightly different corner */
    }
    .model-message {
        background-color: #f0f0f0; /* Light gray */
        margin-right: auto; /* Aligns to the left */
        text-align: left;
        border-bottom-left-radius: 2px; /* Slightly different corner */
    }
    /* Make chat input stick to the bottom */
    .stApp > header {
        display: none; /* Hide default Streamlit header */
    }
    .stChatInputContainer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background: white;
        border-top: 1px solid #f0f0f0;
        z-index: 1000; /* Ensure it stays on top */
    }
    .stApp {
        padding-bottom: 5rem; /* Add padding to body to prevent overlap with fixed input */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Rashmeet's MCP(Model Context Protocol)")
st.markdown("Your intelligent helper for managing user registrations. Ask me to **register users** or **fetch a list of all existing users**.")

if not GOOGLE_API_KEY:
    st.warning("🚨 Google Gemini API Key not found in .env file. Please set it to proceed.")
    st.stop()
else:
    genai.configure(api_key=GOOGLE_API_KEY) # Configure API key explicitly here

# URL for the MCP server
MCP_SERVER_URL = "http://127.0.0.1:5000" # Default Flask port

# Define the tools for Gemini (types remain uppercase and wrapped in function_declarations within a list of tools)
tools = [
    {
        "function_declarations": [
            {
                "name": "store_user_data",
                "description": "Stores user registration data (name, email, date of birth) in the system. Use YYYY-MM-DD format for DOB (e.g., 1990-01-01).",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "name": { "type": "STRING", "description": "The full name of the user." },
                        "email": { "type": "STRING", "description": "The email address of the user." },
                        "dob": { "type": "STRING", "description": "The date of birth of the user in YYYY-MM-DD format." }
                    },
                    "required": ["name", "email", "dob"]
                }
            }
        ]
    },
    {
        "function_declarations": [
            {
                "name": "fetch_all_users",
                "description": "Fetches and returns a list of all registered users with their name, email, and date of birth.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {}
                }
            }
        ]
    }
]

# Initialize the Gemini model with tools
if 'model' not in st.session_state:
    st.session_state.model = genai.GenerativeModel("gemini-1.5-flash", tools=tools)

# Initialize chat history in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "model", "text": "Hello! I'm your Registration Assistant. I can help you **register new users** (e.g., *'Register John Doe with john@example.com born 1990-01-01'*) or **fetch a list of all existing users** (*'Show me all registered users'*). What would you like to do?"})

# Initialize chat object in session state
if 'chat' not in st.session_state:
    chat_history_for_gemini = []
    for msg in st.session_state.messages:
        # Only include user and model text messages for Gemini's history
        if msg["role"] in ["user", "model"]:
            chat_history_for_gemini.append({
                "role": msg["role"],
                "parts": [{"text": msg["text"]}]
            })
    st.session_state.chat = st.session_state.model.start_chat(
        enable_automatic_function_calling=True,
        history=chat_history_for_gemini
    )

def call_mcp_tool(tool_name, **kwargs):
    """
    Calls an MCP server tool via HTTP request.
    Returns the JSON response or an error dictionary.
    """
    endpoint = f"{MCP_SERVER_URL}/{tool_name}"
    st.info(f"DEBUG: Calling MCP server: {endpoint} with args: {kwargs}") # Debugging message
    try:
        response = requests.post(endpoint, json=kwargs)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        st.info(f"DEBUG: MCP server raw response status: {response.status_code}") # Debugging message
        st.info(f"DEBUG: MCP server raw response data: {response.text}") # Debugging message
        return response.json()
    except requests.exceptions.RequestException as e:
        # User-friendly error for server connection
        st.error(f"⚠️ **Connection Error:** Could not reach the Registration Server. Please ensure '`python server/server.py`' is running in a separate terminal. Details: {e}")
        return {"error": f"Server connection error: {e}"}

# Display chat messages from history on app rerun
# This loop now renders the messages with custom styling
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-bubble user-message">{message["text"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "model":
        st.markdown(f'<div class="chat-bubble model-message">{message["text"]}</div>', unsafe_allow_html=True)
    # Tool messages are handled internally and not displayed as chat bubbles

# User input section at the bottom
# This allows the chat input to stay visible as history grows
with st.container():
    prompt = st.chat_input("Ask me anything about registrations...")

if prompt:
    st.session_state.messages.append({"role": "user", "text": prompt})
    # Display the user's message immediately
    st.markdown(f'<div class="chat-bubble user-message">{prompt}</div>', unsafe_allow_html=True)

    with st.spinner("Processing your request..."):
        llm_response = None
        try:
            st.info("DEBUG: Calling Gemini API for initial response...") # Debugging message
            llm_response = st.session_state.chat.send_message(prompt)
            st.info("DEBUG: Gemini API call completed. Checking response...") # Debugging message
        except Exception as e:
            st.error(f"An error occurred while communicating with Gemini. Please check your API key and try again. Error: {e}")
            st.session_state.messages.append({"role": "model", "text": "I encountered an error communicating with Gemini. Please try again later."})
            st.markdown(f'<div class="chat-bubble model-message">I encountered an error communicating with Gemini. Please try again later.</div>', unsafe_allow_html=True)
            # No st.stop() here so user can try again
            st.rerun() # Use st.rerun instead of st.experimental_rerun

        model_responded = False
        
        # Check if candidates exist and have content parts
        if llm_response and llm_response.candidates and llm_response.candidates[0].content.parts:
            for content_part in llm_response.candidates[0].content.parts:
                # Handle text response from Gemini
                if hasattr(content_part, 'text') and content_part.text:
                    st.info(f"DEBUG: Gemini responded with text.") # Debugging message
                    st.session_state.messages.append({"role": "model", "text": content_part.text})
                    st.markdown(f'<div class="chat-bubble model-message">{content_part.text}</div>', unsafe_allow_html=True)
                    model_responded = True
                
                # Handle function call from Gemini
                elif hasattr(content_part, 'function_call') and content_part.function_call:
                    tool_call = content_part.function_call
                    tool_name = tool_call.name
                    tool_args = tool_call.args
                    st.warning(f"DEBUG: Gemini identified a function call: `{tool_name}` with args: `{tool_args}`") # Debugging message

                    # Instead of showing raw tool call, indicate action
                    st.info(f"✅ **Assistant is taking action:** `{tool_name.replace('_', ' ').title()}`...")

                    tool_output = None
                    if tool_name == "store_user_data":
                        tool_output = call_mcp_tool(tool_name, **tool_args)
                        if tool_output and tool_output.get("status") == "success":
                            st.success(f"🥳 **Success!** User '{tool_args.get('name', 'N/A')}' has been registered.")
                            # Gemini's follow-up message will be generated based on this
                        elif tool_output and tool_output.get("error"):
                            st.error(f"😔 **Registration Failed:** {tool_output.get('message', tool_output.get('error', 'Unknown error.'))}")

                    elif tool_name == "fetch_all_users":
                        tool_output = call_mcp_tool(tool_name)
                        if tool_output and tool_output.get("status") == "success":
                            users = tool_output.get("users", [])
                            if users:
                                st.success("📋 **Here are the registered users:**")
                                st.dataframe(users, use_container_width=True) # Display users in a nice table
                                # Add a summary to the chat history that Gemini can see for context
                                # FIX: Use 'Name' (capital N) as per CSV structure
                                user_summary = "\n".join([f"- {u.get('Name', 'N/A')} ({u.get('email', 'N/A')})" for u in users])
                                st.session_state.messages.append({"role": "model", "text": f"Found {len(users)} registered users:\n{user_summary}"}) # User-facing message
                            else:
                                st.info("ℹ️ **No users registered yet.**")
                                # Add to chat history
                                st.session_state.messages.append({"role": "model", "text": "No users registered yet."})
                        elif tool_output and tool_output.get("error"):
                            st.error(f"😔 **Failed to fetch users:** {tool_output.get('message', tool_output.get('error', 'Unknown error.'))}")
                    
                    else: # Fallback for unexpected tool names
                        st.error(f"🤔 **Error:** Assistant tried to call an unknown tool: `{tool_name}`.")
                        tool_output = {"error": f"Unknown tool: {tool_name}"}
                    
                    # Send tool output back to Gemini for context and a final response
                    if tool_output is not None:
                        st.info(f"DEBUG: MCP server response for tool: {tool_output}") # Debugging message
                        # Store tool output in history for internal use (not displayed as a chat bubble)
                        st.session_state.messages.append({"role": "tool", "text": json.dumps(tool_output)})

                        with st.spinner("Generating final response..."):
                            st.info("DEBUG: Sending tool output back to Gemini for follow-up...") # Debugging message
                            try:
                                # Construct the function response using proto objects for robustness
                                function_response_proto = genai_protos.FunctionResponse(
                                    name=tool_name,
                                    response=tool_output # The response should be the dict directly
                                )
                                tool_response_part = genai_protos.Part(function_response=function_response_proto)
                                tool_response_content = genai_protos.Content(
                                    role="function", # Role for tool responses in chat history
                                    parts=[tool_response_part]
                                )

                                gemini_follow_up_response = st.session_state.chat.send_message(tool_response_content)
                                st.info(f"DEBUG: Gemini follow-up response received: {gemini_follow_up_response.candidates[0].content.parts if gemini_follow_up_response.candidates else 'No candidates'}") # Debugging message

                                if gemini_follow_up_response.candidates and gemini_follow_up_response.candidates[0].content.parts:
                                    for follow_up_content_part in gemini_follow_up_response.candidates[0].content.parts:
                                        if hasattr(follow_up_content_part, 'text') and follow_up_content_part.text:
                                            # Only add model's follow-up text if it's new and meaningful
                                            # Avoids redundant "registered successfully" if the success message already covered it
                                            st.session_state.messages.append({"role": "model", "text": follow_up_content_part.text})
                                            st.markdown(f'<div class="chat-bubble model-message">{follow_up_content_part.text}</div>', unsafe_allow_html=True)
                                            model_responded = True
                                        elif hasattr(follow_up_content_part, 'function_call') and follow_up_content_part.function_call:
                                            st.warning("🔄 **Assistant wants to perform another action.** This demo does not recursively handle chained tool calls. Please make a new request.")
                                            model_responded = True
                                    if not model_responded:
                                        # Fallback if follow-up from Gemini is not text or a new function call
                                        st.error("😔 Assistant completed the action, but didn't provide a clear final message. Please try a different request.")
                                        st.session_state.messages.append({"role": "model", "text": "I completed the action, but I didn't get a clear follow-up message from the AI. Can you ask something else?"})
                                        st.markdown(f'<div class="chat-bubble model-message">I completed the action, but I didn\'t get a clear follow-up message from the AI. Can you ask something else?</div>', unsafe_allow_html=True)
                                else:
                                    st.error("😔 Assistant received an empty or malformed follow-up from Gemini. Please try again.")
                                    st.session_state.messages.append({"role": "model", "text": "The AI provided an empty or malformed follow-up. Please try again."})
                                    st.markdown(f'<div class="chat-bubble model-message">The AI provided an empty or malformed follow-up. Please try again.</div>', unsafe_allow_html=True)

                            except Exception as e:
                                st.error(f"An unexpected error occurred during follow-up processing: {e}")
                                st.session_state.messages.append({"role": "model", "text": f"An unexpected error occurred during follow-up: {e}"})
                                st.markdown(f'<div class="chat-bubble model-message">An unexpected error occurred during follow-up processing.</div>', unsafe_allow_html=True)
                    model_responded = True # A tool action was attempted, so consider it "responded"
        
        if not model_responded:
            # Fallback for cases where neither text nor function_call was found initially
            st.error("😕 **I'm having trouble understanding that.** Please rephrase your request or try a different command.")
            st.session_state.messages.append({"role": "model", "text": "I'm having trouble understanding that. Please rephrase your request."})
            st.markdown(f'<div class="chat-bubble model-message">I\'m having trouble understanding that. Please rephrase your request.</div>', unsafe_allow_html=True)

    # Rerun the app to ensure all new messages and UI elements are rendered
    st.rerun() # Replaced st.experimental_rerun with st.rerun
