import json

from CategoryBot import CategoryBot
from ExplanationRetriever import ExplanationRetriever
from acronyms import acronyms
from fetching.model import get_data

async def choose_data(state):
    
    websocket = state["websocket"]
    category = state["category"]
    request = state["request"]
    thread_history = state["thread_history"]
    loop = state["loop"]
    thread_id = state["thread_id"]
    
    data_choice = await handle_data_choice(
        websocket, category, request, thread_history, loop, thread_id
    )
    choice = data_choice["choice"]
    explanation = data_choice["explanation"]
    
    state["data_choice"] = choice
    state["data_choice_explanation"] = explanation

    data = []

    for key, params in choice.items():
        # In case one type of data is supposed to be retrieved with several parameter configurations
        if isinstance(params, list):
            for param in params:
                data = await handle_data_append(
                    data, category, key, param, loop
                )

        else:
            data = await handle_data_append(data, category, key, params, loop)
            
    state["data"] = data
    
    return state
            
            
            
async def handle_data_choice(websocket, category, request, history, loop, thread_id):
    await websocket.send(
        json.dumps(
            {
                "type": "status",
                "text": "Looking for relevant data...",
                "thread_id": thread_id,
            }
        )
    )
    category_bot = CategoryBot(category)
    data_choice = await loop.run_in_executor(
        None, category_bot.handle_request, request, history
    )
    choice_response = data_choice["response"]
    choice_explanation = data_choice["explanation"]
    await websocket.send(
        json.dumps(
            {
                "type": "data_choice",
                "choice": choice_response,
                "explanation": choice_explanation,
                "thread_id": thread_id,
            }
        )
    )

    return {"choice": choice_response, "explanation": choice_explanation}


async def handle_data_append(data, category, key, param, loop):
    explanation_retriever = ExplanationRetriever()
    available_keys = acronyms.keys()
    validated_key = None
    if key not in available_keys:
        for my_key in available_keys:
            if my_key in key:
                validated_key = my_key
                break
    else:
        validated_key = key
    if validated_key == None:
        return data
    data.append(
        {
            "data": await loop.run_in_executor(
                None, get_data, category.lower(), validated_key, param
            ),
            "explanation": await loop.run_in_executor(
                None, explanation_retriever.get_explanation, validated_key
            ),
        }
    )

    return data