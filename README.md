AI Agent Backend Workspace 🤖

An autonomous, multi-tool agentic system built using the modern LangChain ecosystem, Pydantic, and vector databases. This workspace tracks a rigorous, hands-on engineering journey from basic LLM prompts to self-correcting agent loops that manipulate mock databases and dispatch communication signals.

🗺️ Engineering Progression (Weeks 1-5)

This repository serves as a portfolio of foundational AI concepts developed systematically:

Week 1 (API Fundamentals): Python-based API communication, environment isolation, and error-handling pipelines.

Week 2 (Schema Enforcement): Enforcing strict output structuralization using Pydantic models to guarantee programmatically reliable system inputs.

Week 3 (Vector Mathematics): Implementing raw, mathematical cosine-similarity calculations over raw text embeddings.

Week 4 (RAG Pipeline): An enterprise-grade Retrieval-Augmented Generation pipeline using ChromaDB to index and query localized context databases.

Week 5 (Autonomous Agents & Tool Calling): An orchestration layer executing multi-step reasoning utilizing LangChain Classic agent structures and dynamic function tools.

🛠️ Tech Stack & Dependencies

Runtime: Python 3.12+

Framework: LangChain & LangChain-Classic (v0.3 architecture compatible)

LLM Provider: OpenAI GPT-4o-mini

Environment Management: python-dotenv & .venv isolation

Schema & Math: pydantic, numpy (for vector operations)

Vector Indexing: chromadb

📦 Architecture Overview

The core file, agent_workflow.py, contains an autonomous loop running with two specialized, decorator-injected local system tools:

fetch_order_status: Queries an internal mock database for shipping schedules and courier tracking IDs.

send_support_escalation_email: Dispatches high-priority support emails when the agent registers user frustration.

                  ┌──────────────────────────────┐
                  │      User Conversation       │
                  └──────────────┬───────────────┘
                                 ▼
                     ┌───────────────────────┐
                     │   LangChain Agent     │
                     └───────────┬───────────┘
                                 ▼
                    [Reasoning & Tool Selection]
                                 │
         ┌───────────────────────┴───────────────────────┐
         ▼                                               ▼
┌──────────────────┐                            ┌──────────────────┐
│fetch_order_status│                            │send_support_email│
└────────┬─────────┘                            └────────┬─────────┘
         │                                               │
         └───────────────────────┬───────────────────────┘
                                 ▼
                     ┌───────────────────────┐
                     │ Final Agent Response  │
                     └───────────────────────┘



🚀 Setup & Installation

1. Clone & Navigate

Navigate to your backend directory:

cd ai-backend



2. Configure Virtual Environment

Create and activate your Python virtual environment:

python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate



3. Install Dependencies

Install the required packages:

pip install langchain langchain-classic langchain-openai python-dotenv chromadb pydantic



4. Set Environment Variables

Create a .env file in the root of the ai-backend directory:

OPENAI_API_KEY=your-actual-api-key-here



5. Run the Workflow

Execute the autonomous agent loop:

python agent_workflow.py



🌟 Sample Execution Logs

When you execute the agent, you will watch it evaluate natural language, select your tools, extract parameters, and execute code locally:

🚀 STARTING AGENT SCENARIO A: 'Hey, can you check where my order ORD-1234 is? Thanks!'

⚙️ [SYSTEM TOOL RUNNING] fetch_order_status called for ID: ORD-1234

🤖 FINAL AI AGENT RESPONSE A:
Your order (ORD-1234) has shipped yesterday via FedEx.
The tracking number is 1Z999AA10123456784, and expected delivery is this Tuesday.

