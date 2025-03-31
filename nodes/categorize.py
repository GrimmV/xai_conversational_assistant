import json
from typing import Tuple
from CategoryRoutingBot import CategoryRoutingBot

async def categorize(state):
    
    thread_category = state["thread_category"]
    websocket = state["websocket"]
    request = state["request"]
    history = state["history"]
    loop = state["loop"]
    
    if thread_category:
        category = thread_category
        state["category"] = category
        state["cat_explanation"] = "Thread category"
    else:
        cat_and_explanation = await handle_category_routing(
            websocket, request, history["general"], loop
        )
        state["category"] = cat_and_explanation["category"]
        state["cat_explanation"] = cat_and_explanation["explanation"]
        
    return state
    
    
async def handle_category_routing(websocket, request, history, loop):
    await websocket.send(json.dumps({"type": "status", "text": "Choosing category..."}))
    category_router = CategoryRoutingBot()

    routing_response = await loop.run_in_executor(
        None, category_router.handle_request, request, history
    )

    category = routing_response["category"]
    category_explanation = routing_response["explanation"]
    await websocket.send(
        json.dumps(
            {
                "type": "routing",
                "category": category,
                "explanation": category_explanation,
            }
        )
    )

    return {"category": category, "explanation": category_explanation}