import json
from config import max_hist

from GuidanceBot import GuidanceBot

async def guidance_response(state):
    
    history = state["history"]
    websocket = state["websocket"]
    request = state["request"]
    loop = state["loop"]
    thread_id = state["thread_id"]
    
    lookback_hist = history["general"][-max_hist:]
    response = await handle_guidance(
        websocket, request, lookback_hist, loop, thread_id
    )
    
    state["final_resp"] = response["response"]
    state["final_resp_explanation"] = response["explanation"]
    
    return state
    
    
async def handle_guidance(websocket, request, history, loop, thread_id=None):
    guidance_bot = GuidanceBot()
    guidance_response = await loop.run_in_executor(
        None, guidance_bot.handle_request, request, history
    )
    response = guidance_response["response"]
    explanation = guidance_response["explanation"]
    await websocket.send(
        json.dumps(
            {
                "type": "response",
                "response": response,
                "explanation": explanation,
                "thread_id": thread_id
            }
        )
    )

    return {"response": response, "explanation": explanation}