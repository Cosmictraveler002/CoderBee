# FastAPI router with StreamingResponse
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.utils.httpx_client import query_llm , stream_query_llm
from app.schemas import ChatRequest
from fastapi.responses import StreamingResponse

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
    
@app.post("/chat/stream")
async def stream_chat(request: ChatRequest):
    async def event_generator():
            async for token in stream_query_llm(
                request.prompt,
                model='gemma4',
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            ):
                yield f"data:{token}\n\n"

            return StreamingResponse(event_generator(), media_type="text/event-stream")