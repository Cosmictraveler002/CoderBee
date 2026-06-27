import httpx

LLM_ENDPOINT = "http://localhost:11434/api/generate"   
DEFAULT_MODEL = "gemma4"

async def query_llm(prompt: str, model: str = DEFAULT_MODEL) -> str:
   
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(LLM_ENDPOINT, json=payload, timeout=60.0)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", str(data))