# FastAPI router with StreamingResponse
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.utils.httpx_client import query_llm
from app.schemas import ChatRequest

app = FastAPI(title="AI Memory Server")

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response_text = await query_llm(
            request.prompt,
            model='gemma4',
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        return {"response": response_text}
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={"error": f"LLM query failed: {str(e)}"}
        )