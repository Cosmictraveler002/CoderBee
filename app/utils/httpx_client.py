import httpx
import json

LLM_ENDPOINT = "http://localhost:11434/api/generate"   
DEFAULT_MODEL = "gemma4"

async def query_llm(
    prompt: str,
    model: str = 'gemma4',
    max_tokens: int = 512,
    temperature: float = 0.7,
) -> str:
   
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": temperature,
        },
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(LLM_ENDPOINT, json=payload, timeout=60.0)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", str(data))
    
async def stream_query_llm(prompt:str, model:str ='gemma4',   max_tokens: int = 512, temperature: float = 0.7,):
    payload = {
        "model":model,
        "prompt":prompt,
        "stream":True,
        "options": {
            "num_predict": max_tokens,
            "temperature": temperature,
        }
    }

    async with httpx.AsyncClient.stream("POST") as client:
        async with client.stream("POST", LLM_ENDPOINT, json=payload, timeout=60.0) as response:
            response.raise_for_status()
            async for lines in response.aiter_lines():
                if not lines.strip():
                    continue
                try:
                    data = json.loads(lines)
                    if data.get("done"):
                        break
                    token = data.get("response", "")
                    if token:
                        yield token
                except json.JSONDecodeError:
                    continue
