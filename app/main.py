"# FastAPI router with StreamingResponse" 
from fastapi import FastAPI
from pydantic import BaseModel
from app.utils.httpx_client import query_llm

class ChatRequest(BaseModel):
    prompt: str
    model: str = "gemma4"


app = FastAPI(title="AI Memory Server")

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response_text = await query_llm(request.prompt, request.model)
        return {"response": response_text}
    except Exception as e:
        return {"error": f"LLM query failed: {str(e)}"}