# Gemini MCP Registration App

This is a demo project that uses **Google Gemini 1.5 Flash** to interact with an **MCP (Model Calling Protocol)** server. The MCP server exposes tools (functions) like storing and fetching user data, which Gemini can call directly through tool-use.


## Project Features

- Register users by storing their data (name, email, DOB) in a CSV file.
- Fetch all stored users.
- Gemini automatically decides when to call the tools.
- Supports natural language instructions like:
- "Register a user named Sachin with email sachin@gmail.com and DOB 2002-01-01"

## How to Run

### 1. Start the MCP Server

```bash
python server/server.py