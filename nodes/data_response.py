import json
from ResponseBot import ResponseBot

async def data_response(state):
    
    websocket = state["websocket"]
    request = state["request"]
    data = state["data"]
    thread_history = state["thread_history"]
    loop = state["loop"]
    thread_id = state["thread_id"]
    
    response = await handle_final_response(
        websocket, request, data, thread_history, loop, thread_id
    )
    
    state["final_resp"] = response["response"]
    state["final_resp_explanation"] = response["explanation"]
    
    return state
    
    
async def handle_final_response(websocket, request, data, history, loop, thread_id):

    await websocket.send(
        json.dumps(
            {
                "type": "status",
                "text": "Produce final response...",
                "thread_id": thread_id,
            }
        )
    )
    response_bot = ResponseBot()
    final_response = await loop.run_in_executor(
        None, response_bot.handle_request, request, data, history
    )

    response = final_response["response"]
    explanation = final_response["explanation"]

    await websocket.send(
        json.dumps(
            {
                "type": "response",
                "response": response,
                "explanation": explanation,
                "thread_id": thread_id,
            }
        )
    )

    return {"response": response, "explanation": explanation}