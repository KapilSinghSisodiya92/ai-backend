import asyncio
import os
import json
from dotenv import load_dotenv
from httpx import AsyncClient
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal

load_dotenv()

# 1. Define our Frontend Component Schema (Like a Zod Schema / TS Interface)
class UIComponent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    component_type: Literal["Button", "Input", "Card", "Heading"] = Field(
        description="The type of UI component to render."
    )
    label: str = Field(description="The visible text or placeholder for the component.")
    variant: Literal["primary", "secondary", "danger", "outline"] = Field(
        description="The design system variant style."
    )
    flex_width: str = Field(description="Tailwind width class, e.g., 'w-full' or 'w-1/2'.")

class UILayout(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    layout_title: str = Field(description="A catchy title for this layout container.")
    components: List[UIComponent] = Field(description="An array of components ordered sequentially.")

# 2. Set up our AI Generator Logic
async def generate_ui_layout(user_description: str):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('LLM_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    # We pass the Pydantic schema structure directly into OpenAI's 'response_format'
    payload = {
        "model": "gpt-4o-mini",  # Fast, highly accurate for structured outputs
        "messages": [
            {
                "role": "system", 
                "content": "You are a senior UI/UX designer. Translate user layout requests into clean, semantic component data structures."
            },
            {
                "role": "user", 
                "content": f"Generate a layout for: {user_description}"
            }
        ],
        # THIS IS THE MAGIC: We force OpenAI to use our Pydantic schema
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "ui_layout_schema",
                "strict": True,
                "schema": UILayout.model_json_schema()
            }
        },
        "temperature": 0.2 # Low temperature = less creativity, more strict adherence to rules
    }

    async with AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers, timeout=30.0)
        
        if response.status_code == 200:
            raw_content = response.json()['choices'][0]['message']['content']
            # Parse the clean string text into a true Python dictionary/JSON object
            structured_json = json.loads(raw_content)
            return structured_json
        else:
            return f"Error: {response.status_code} - {response.text}"

async def main():
    # Prompting a complex dashboard requirements chunk
    sample_request = "I need a standard login form layout. It should have a heading, an email input field, a password input field, and a blue submit button."
    
    result = await generate_ui_layout(sample_request)
    
    print("💎 Perfectly Structured JSON Output for Frontend Mapping:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())