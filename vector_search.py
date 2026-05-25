import asyncio
import os
import numpy as np
from dotenv import load_dotenv
from httpx import AsyncClient

load_dotenv()

# 1. Helper function to turn text into a vector array using OpenAI
async def get_embedding(text: str, client: AsyncClient) -> list:
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {os.getenv('LLM_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-embedding-3-small",
        "input": text
    }
    
    response = await client.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        # Extract the array of numbers
        return response.json()['data'][0]['embedding']
    else:
        raise Exception(f"Failed to fetch embedding: {response.text}")

# 2. Math helper: Calculate Cosine Similarity between two vectors
def calculate_similarity(vec_a, vec_b):
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    return dot_product / (norm_a * norm_b)

# 3. Main Search Engine Setup
async def main():
    # Mock data store: Internal Documentation for a company's frontend code guidelines
    knowledge_base = [
        "Use Tailwind CSS utility classes for styling. Do not write vanilla CSS or styled-components.",
        "Always use TypeScript interfaces instead of types for defining object schemas.",
        "State management should favor React Context for global UI states, and Zustand for heavy server data.",
        "Deploy all frontend micro-frontends onto AWS CloudFront using S3 static website hosting buckets."
    ]
    
    async with AsyncClient() as client:
        print("⏳ Generating vector embeddings for the knowledge base...")
        # Convert all our text strings into vector numbers
        embedded_database = []
        for text in knowledge_base:
            vector = await get_embedding(text, client)
            embedded_database.append({"text": text, "vector": vector})
            
        print("✅ Knowledge Base Vectorized!\n")
        
        # Simulated User Search Query
        user_query = "What is the best deployment strategy on Amazon Web Services?"
        print(f"🔍 User Search Query: '{user_query}'")
        
        # Turn user query into a vector too!
        query_vector = await get_embedding(user_query, client)
        
        # Compare user query vector against every single vector in our database
        results = []
        for item in embedded_database:
            score = calculate_similarity(query_vector, item["vector"])
            results.append({"text": item["text"], "score": score})
            
        # Sort results so the highest mathematical score is at the top
        results.sort(key=lambda x: x["score"], reverse=True)
        
        print("\n🏆 Top Semantic Search Matches:")
        for idx, match in enumerate(results[:2], 1):
            print(f"Rank {idx} (Similarity Score: {match['score']:.4f}):")
            print(f" 👉 \"{match['text']}\"\n")

if __name__ == "__main__":
    asyncio.run(main())