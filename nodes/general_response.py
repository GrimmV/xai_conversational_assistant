import json
from config import max_hist

from GeneralBot import GeneralBot

async def general_response(state):
    
    history = state["history"]
    websocket = state["websocket"]
    request = state["request"]
    loop = state["loop"]
    thread_id = state["thread_id"]
    
    general_history = history["general"]
    # Only take the last three elements from the history as a general response should not be
    # dependend on a large chunk of the conversation history
    lookback_hist = general_history[-max_hist:]
    response = await handle_general(websocket, request, lookback_hist, loop, thread_id)
    
    state["final_resp"] = response["response"]
    state["final_resp_explanation"] = response["explanation"]
    
    return state

async def handle_general(websocket, request, history, loop, thread_id=None):
    general_bot = GeneralBot()
    general_response = await loop.run_in_executor(
        None, general_bot.handle_request, request, history
    )
    await websocket.send(
        json.dumps(
            {
                "type": "response",
                "response": general_response["response"],
                "explanation": general_response["explanation"],
                "thread_id": thread_id
            }
        )
    )
    response = general_response["response"]
    explanation = general_response["explanation"]

    return {"response": response, "explanation": explanation}