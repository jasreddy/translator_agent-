# Gemini Translator Agent

This repository contains a AI-powered translation agent. it's an agent designed to be run within the [**GenAI AgentOS**](https://github.com/genai-works-org/genai-agentos/tree/main) framework.

This agent leverages Google's advanced **Gemini 2.5 Flash** model to provide translations that are   accurate and also fluent and context-aware.



---

## 🚀 Quick Start: How to Run This Agent

Running this agent involves two main parts:
1.  **Setting up the GenAI AgentOS Infrastructure**: This provides the "brain" (Master Agent) and the communication server.
2.  **Running the Translator Agent**: This script connects to the infrastructure as a specialized tool.

### Step 1: Set Up the GenAI AgentOS Infrastructure

The translator agent needs the central `genai-agentos` server to connect to. You must have this running first.

1.  **Clone the GenAI AgentOS repository:**
    ```bash
    git clone https://github.com/genai-works-org/genai-agentos.git

2.  **Navigate into the directory:**
    ```bash
    cd genai-agentos/
    ```

3.  **Start the infrastructure using Docker Compose:**
    This command will build and run all the necessary services, including the Master Agent, the WebSocket server, and the frontend UI.
    ```bash
    docker compose up
    ```

4.  **Verify the UI is running:**
    Once the services are up, you can access the frontend UI in your browser at:
    **[http://localhost:3000/](http://localhost:3000/)**

### Step 2: Prepare Your Environment for the Agent

Now, let's set up the environment for this translator agent.

1.  **Clone this repository** (if you haven't already).
    ```bash
    git clone <URL_to_this_translator_agent_repo>
    cd <translator_agent_repo_directory>
    ```

2.  **Install the required Python packages:**
    This project uses a `requirements.txt` file to manage its dependencies.
    ```bash
    uv venv env --python 3.12
    uv pip install -r requirements.txt
    ```

3.  **Create your `.env` file:**
    The agent needs your Google API key to make calls to the Gemini model. Create a file named `.env` in the root of this project folder.
    ```
    # .env
    GOOGLE_API_KEY="PASTE_YOUR_GEMINI_API_KEY_HERE"
    ```
    You can get a free API key from Google AI Studio.

### Step 3: Register the Agent and Get a JWT Token

Before running the agent, you must register it with the running `genai-agentos` system. This requires the `genai-cli` tool from the `genai-agentos` repository.

1.  **Install the `genai-cli`:**
    this is already installed in requirements 

2.  **Sign up and log in:**
    If you already have a GenAI account (from front-end or back-end):

    ```bash
    genai login -u <your_username> -p <your_password>
    ```

    First-time users:
    ```bash
    genai signup -u <new_username>
    ```

3.  **Register this agent:**
    The `register_agent` . This token is crucial.
    ```bash
    genai register_agent --name "translate_text" --description "Translate text from one language to another."
    python3 cli.py list_agents
    ```
    
    **Copy the JWT Token that is printed to your clipboard.**

### Step 4: Run the Translator Agent

You're now ready to run the agent!

1.  **Update the Agent Code with Your JWT Token:**
    Open the `agent.py` file (or the main agent script) in this repository. Find the `session = GenAISession(...)` line and paste your copied JWT token.

    ```python
    # agent.py
    session = GenAISession(
        jwt_token="PASTE_YOUR_JWT_TOKEN_HERE",
        ws_url="ws://localhost:8080/ws"
    )
    ```

2.  **Run the agent script:**
    ```bash
    python3 main.py
    ```

    You should see a message indicating that the agent is running and waiting for tasks:
    ```
    Gemini Translator Agent (using new google-genai SDK) is running.
    Waiting for the orchestrator to assign translation tasks...
    ```

### Step 5: Use the Agent

Go to the **Frontend UI at [http://localhost:3000/](http://localhost:3000/)** and start a new chat. Ask it to perform a translation. The Master Agent will now see your running `translate_text` tool and delegate the task to it.

**Example Prompts:**

- "Translate 'it's raining cats and dogs' from English to French."
- "How do you say 'this is a piece of cake' in Spanish?"
- "What is 'Wie geht es Ihnen?' in English?"
