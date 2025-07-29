✨ Gemini Registration Assistant ✨
Effortless User Management with AI Magic!
Welcome to the Gemini Registration Assistant, a cutting-edge demo project that brings the power of Google Gemini 1.5 Flash directly to your user management tasks. Say goodbye to manual data entry and hello to intuitive, natural language commands!

This application demonstrates how a sophisticated AI model can seamlessly integrate with a custom backend via the Model Calling Protocol (MCP), allowing you to register new users and retrieve existing records with simple conversational prompts.

🌟 Key Features
🗣️ Natural Language Interface: Interact with the system using everyday language – just like talking to a smart assistant!

🧠 Intelligent Tool Use: Gemini 1.5 Flash automatically understands your intent and intelligently decides when and how to call the necessary backend functions.

🚀 Streamlit Frontend: A sleek, interactive web interface designed for a delightful user experience.

💾 Robust Data Management: Securely store and retrieve user data (Name, Email, Date of Birth) in a simple CSV database.

⚡ Flask-Powered Backend: A lightweight and efficient API server (MCP server) that exposes the core registration and fetching functionalities.

🏛️ Architecture Overview
The Gemini Registration Assistant operates on a powerful, yet elegant, multi-component architecture, ensuring clear separation of concerns and robust communication.

graph TD
    A[User's Browser] -- Displays UI --> B(Streamlit Frontend:<br>client/llm.py)
    B -- Sends Text Prompts --> C(Google Gemini 1.5 Flash API)
    C -- 🔄 Intelligent Decision Making 🔄 --> C
    C -- If Tool Required (e.g., register, fetch) --> D{Tool Call Request:<br>JSON format}
    D -- HTTP POST Request --> E(MCP Backend Server:<br>server/server.py)
    E -- Delegates to Local Function --> F(Backend Tools:<br>server/tools/<br>fetch.py, store.py)
    F -- Interacts with --> G(CSV Data Storage:<br>data/registration.csv)
    F -- Returns Tool Output (JSON) --> E
    E -- Returns Tool Output (JSON) --> C
    C -- Processes Tool Output & Generates NL Response --> B
    B -- Displays Response (Text / Data Table) --> A

    style A fill:#e0f2f7,stroke:#3498db,stroke-width:2px,color:#2c3e50;
    style B fill:#d0f0c0,stroke:#2ecc71,stroke-width:2px,color:#2c3e50;
    style C fill:#ffeeba,stroke:#f1c40f,stroke-width:2px,color:#2c3e50;
    style D fill:#f2e0f7,stroke:#9b59b6,stroke-width:2px,color:#2c3e50;
    style E fill:#f0f7e0,stroke:#27ae60,stroke-width:2px,color:#2c3e50;
    style F fill:#e0f7f2,stroke:#1abc9c,stroke-width:2px,color:#2c3e50;
    style G fill:#f7e0e0,stroke:#e74c3c,stroke-width:2px,color:#2c3e50;

User Interface (Streamlit): Your interactive chat window. This is where you type commands and see the AI's responses.

Gemini 1.5 Flash (AI Brain): The core intelligence. It understands what you want, chats with you, and decides when to call a backend "tool" (function) to perform an action.

MCP Backend Server (Flask): The bridge between Gemini and your actual data operations. It receives tool call requests from Gemini (via the Streamlit client), executes the corresponding function, and sends the results back.

Backend Tools (fetch.py, store.py): These are the Python functions that perform the real work: reading from or writing to your registration.csv file.

CSV Data Storage (registration.csv): Your simple database where all user information is kept.

🚀 How It Works: The Magic Behind the Scenes
Let's walk through a typical user interaction to see the pieces in action:

graph TD
    A[1. User Types Request:<br>"Register John Doe with john@example.com born 1990-01-01"] --> B(2. Streamlit Client Sends Prompt to Gemini API)
    B --> C{3. Gemini Analyzes Prompt &<br>Identifies "store_user_data" Tool}
    C --> D[4. Gemini Responds with Tool Call Instruction (JSON)]
    D --> E(5. Streamlit Client Receives Instruction & Makes HTTP POST Request to MCP Server:<br> `/store_user_data` with data)
    E --> F{6. MCP Server Calls `store_user_data` function in `server/tools/store.py`}
    F --> G[7. `store.py` Appends Data to `data/registration.csv`]
    G --> H[8. `store.py` Returns Success/Error to MCP Server]
    H --> I[9. MCP Server Returns JSON Response to Streamlit Client]
    I --> J(10. Streamlit Client Sends Tool Output Back to Gemini)
    J --> K{11. Gemini Processes Tool Output & Generates Natural Language Follow-up}
    K --> L[12. Gemini Responds with Final Text Message]
    L --> M(13. Streamlit Client Displays Success Message/Data Table)

    style A fill:#aed6f1,stroke:#3498db;
    style B fill:#fdfd96,stroke:#f1c40f;
    style C fill:#9fe2bf,stroke:#2ecc71;
    style D fill:#c39bd3,stroke:#8e44ad;
    style E fill:#f5cba7,stroke:#e67e22;
    style F fill:#aeb6bf,stroke:#7f8c8d;
    style G fill:#ffb3ba,stroke:#e74c3c;
    style H fill:#aeb6bf,stroke:#7f8c8d;
    style I fill:#f5cba7,stroke:#e67e22;
    style J fill:#fdfd96,stroke:#f1c40f;
    style K fill:#9fe2bf,stroke:#2ecc71;
    style L fill:#c39bd3,stroke:#8e44ad;
    style M fill:#d0f0c0,stroke:#2ecc71;

This elegant dance between the user, the AI, and your backend tools ensures a smooth and intelligent interaction for all your registration needs!

🛠️ Setup & Running
Get this powerful assistant running on your local machine in just a few steps!

Prerequisites
Python 3.9+ (recommended)

A Google Gemini API Key: Get one here

1. Project Setup
Clone or create the project structure:
Ensure your local directories and files match this structure:

.
├── .env
├── .python-version
├── pyproject.toml
├── README.md (this file!)
├── requirements.txt
├── uv.lock
├── client/
│   └── llm.py
├── server/
│   ├── server.py
│   └── tools/
│       ├── __init__.py
│       ├── fetch.py
│       └── store.py
└── data/
    └── registration.csv (initially can be empty or just headers)

Add your Gemini API Key:
Open the .env file in your project's root directory and replace the placeholder with your actual API key:

GOOGLE_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"

(Ensure no extra spaces around = and the key is in quotes!)

Create a Virtual Environment (Highly Recommended):

python -m venv venv

Activate the virtual environment:

Windows: .\venv\Scripts\activate

macOS/Linux: source venv/bin/activate

Install Dependencies:
Navigate to the root directory of your project (where requirements.txt is located) in your activated terminal and run:

pip install -r requirements.txt --upgrade --no-cache-dir

(This command ensures you have the correct versions of all libraries, including google-generativeai==0.8.5 and protobuf==3.20.0, which are critical for compatibility.)

2. Run the Application
The application consists of two main parts that need to run concurrently: the MCP Backend Server and the Streamlit Frontend Client.

Start the MCP Backend Server:
Open your first terminal window, navigate to the project's root directory, and run:

python server/server.py

You should see output similar to: * Running on http://127.0.0.1:5000. Keep this terminal window open! This server must remain active for the client to function.

Run the Streamlit Frontend Client:
Open a second terminal window, navigate to the project's root directory, and run:

streamlit run client/llm.py

This command will automatically open your Streamlit application in your default web browser (usually at http://localhost:8501).

💬 Usage Examples
Once the Streamlit app is open in your browser, try these commands in the chat input:

Register a New User:

"Register a user named Jane Doe with email jane.doe@example.com born 1992-07-20"

"Can you add Mike Smith? His email is mike@mail.com and DOB is 1985-03-15."

Fetch All Registered Users:

"Fetch all registered users."

"Show me everyone who's signed up."

"List all users."

Observe the clear success/error messages, and how the "Fetch" command displays user data directly in a table within the chat!

🐛 Troubleshooting
SyntaxError: invalid syntax in server.py:

This indicates stray text (like file paths or section numbers) was copied into your Python file. Carefully open server/server.py and remove any non-code lines, especially around line 51 if previous errors occurred there.

ModuleNotFoundError: No module named 'flask' (or any other module):

This means the required Python package is not installed. Ensure you have activated your virtual environment and run pip install -r requirements.txt --upgrade --no-cache-dir from the project root.

Error: No API_KEY or ADC found.:

Your Gemini API key isn't being loaded. Double-check your .env file in the project's root:

Is the file named exactly .env?

Is the key GOOGLE_API_KEY="YOUR_KEY_HERE" (no spaces around =)?

Did you save the .env file after adding the key?

KeyError: 'name' when fetching users:

This is a case sensitivity issue with column headers in registration.csv. Ensure your server/tools/store.py uses 'Name' (capital 'N') in its HEADERS list and when writing the dictionary to the CSV. Also, ensure your client/llm.py accesses user names using u.get('Name', 'N/A').

"Processing your request..." stuck / No response:

Check server.py terminal: Are there any errors? Is it showing POST requests when you send commands from Streamlit? If not, the client isn't reaching the server.

Check Streamlit terminal for "DEBUG" messages: The st.info("DEBUG: ...") messages are there to trace the execution flow. See where it stops or what error is printed there.

Confirm both server and client are running.

AttributeError related to google.generativeai.types.Part or Content:

These are usually due to google-generativeai and protobuf version conflicts. Rerun pip install -r requirements.txt --upgrade --no-cache-dir with the specific versions in your requirements.txt.

Enjoy interacting with your intelligent Registration Assistant!
