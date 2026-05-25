import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

async def main():
    # 1. Initialize our LLM and Embedding models using LangChain wrappers
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 2. Raw Company Document Data (In production, this would be read from PDFs/Markdown files)
    company_policy_docs = [
        "Policy Tech-202: Employees are allocated a maximum budget of $1,500 every two years to purchase a laptop. MacBook Pro and ThinkPad X1 Carbon are pre-approved options.",
        "Policy HR-501: Remote workers must log into Slack by 9:00 AM EST and remain active until 5:00 PM EST. Core collaboration hours are 10:00 AM to 4:00 PM EST.",
        "Policy Ops-12: Standard health insurance packages cover dental and vision up to 80%. Premium packages cover up to 100% but require a $20 monthly payroll deduction."
    ]

    print("📦 Creating local Vector Database via ChromaDB...")
    # Chroma will automatically convert our text strings to embeddings and store them in memory
    vector_store = Chroma.from_texts(
        texts=company_policy_docs,
        embedding=embeddings
    )
    
    # Turn our vector store into a 'Retriever' that fetches the top 1 most relevant chunk
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})

    # 3. Define the Prompt Structure that binds the Context to the LLM
    # Notice the placeholders {context} and {question}. LangChain will inject data here dynamically.
    system_template = """You are an HR compliance assistant. Answer the user's question using ONLY the trusted context provided below. 
    If you do not know the answer based on the context, say 'I cannot find that information in the company directory.'
    
    Trusted Context:
    {context}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", "{question}")
    ])

    # 4. Construct the LangChain Expression Language (LCEL) Chain
    # This chain handles: Retrieve context -> Pass to prompt -> Send to LLM -> Parse text string
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 5. Let's test our RAG System!
    user_question = "What laptops can I buy and how much can I spend?"
    print(f"\n🙋 User Question: {user_question}")
    
    print("🧠 Retrieving context and generating answer...")
    response = await rag_chain.ainvoke(user_question)
    
    print(f"\n🤖 AI Agent Response:\n{response}\n")

    # Test the safety constraint: Asking something outside the trusted context
    unrelated_question = "What is the policy for vacation days?"
    print(f"🙋 User Question: {unrelated_question}")
    safety_response = await rag_chain.ainvoke(unrelated_question)
    print(f"🤖 AI Agent Response:\n{safety_response}")

if __name__ == "__main__":
    asyncio.run(main())