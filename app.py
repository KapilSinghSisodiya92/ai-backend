import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def call_lmm(user_prompt: str):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('LLM_API_KEY')}"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": user_prompt}]
    }
    print("sending request to LLM")

    async with httpx.AsyncClient() as client:
        try:

            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            
            if response.status_code == 200:
                    result = response.json()
                    # Drillin down into standard OpenAI/Llama response shapes
                    ai_reply = result['choices'][0]['message']['content']
                    return ai_reply
            else:
                return f"Error: Received status code {response.status_code} from provider."
            
        except Exception as e:
            return f"An exception occurred: {str(e)}"
        

async def main():
    user_prompt = "Explain CSS Flexbox vs Grid in one short sentence for a beginner."
    reply = await call_lmm(user_prompt)
    print("\n🤖 AI Response:", reply)

if __name__ == "__main__":
    asyncio.run(main())