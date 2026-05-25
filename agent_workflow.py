import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
# We use standard core prompt tools now - no 'hub' package needed!
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. Define our Mock Database Tools using the @tool decorator
@tool
def fetch_order_status(order_id: str) -> str:
    """Queries the internal database to check the real-time shipping status of a specific order ID."""
    mock_db = {
        "ORD-1234": "Shipped yesterday via FedEx. Tracking number: 1Z999AA10123456784. Expected delivery: Tuesday.",
        "ORD-5678": "Processing. Order received but has not left our warehouse yet."
    }
    print(f"\n⚙️ [SYSTEM TOOL RUNNING] fetch_order_status called for ID: {order_id}")
    return mock_db.get(order_id, f"Order ID {order_id} not found in database.")

@tool
def send_support_escalation_email(user_email: str, issue_summary: str) -> str:
    """Sends an escalation ticket email to human support managers when an order is lost or delayed."""
    print(f"\n⚙️ [SYSTEM TOOL RUNNING] Sending email to support managers...")
    print(f"📧 [EMAIL OUTBOX] To: support@company.com | From: {user_email} | Subject: Escalation - {issue_summary}")
    return "Success: Escalation email ticket has been generated and dispatched to human teams."

async def main():
    # 2. Initialize our LLM 
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 3. Bundle our tools into a list
    tools = [fetch_order_status, send_support_escalation_email]

    # 4. Construct our own Explicit Agent Prompt Template (Bypassing the remote hub!)
    # This structure provides the exact message placeholders that the OpenAI Tools Agent expects.
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful customer support agent. Use the provided tools to answer queries effectively."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad") # Keeps track of the agent's intermediate thoughts/tool responses
    ])

    # 5. Construct the Agent runtime and the Executor loop
    agent = create_openai_tools_agent(llm, tools, agent_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # --- Scenario A: User wants to track their package ---
    user_input_a = "Hey, can you check where my order ORD-1234 is? Thanks!"
    print(f"\n🚀 STARTING AGENT SCENARIO A: '{user_input_a}'")
    
    response_a = await agent_executor.ainvoke({"input": user_input_a})
    print(f"\n🤖 FINAL AI AGENT RESPONSE A:\n{response_a['output']}\n")
    
    print("-" * 50)

    # --- Scenario B: User is frustrated and wants human help ---
    user_input_b = "My order ORD-5678 hasn't shipped yet and I need it for a wedding tomorrow! Email support at alex@test.com and get a human to escalate this immediately."
    print(f"\n🚀 STARTING AGENT SCENARIO B: '{user_input_b}'")
    
    response_b = await agent_executor.ainvoke({"input": user_input_b})
    print(f"\n🤖 FINAL AI AGENT RESPONSE B:\n{response_b['output']}\n")

if __name__ == "__main__":
    asyncio.run(main())