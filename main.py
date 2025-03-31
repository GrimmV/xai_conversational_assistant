from CategoryRoutingBot import CategoryRoutingBot, categories
from CategoryBot import CategoryBot
from GeneralBot import GeneralBot
from ResponseBot import ResponseBot
from GuidanceBot import GuidanceBot
from ExplanationRetriever import ExplanationRetriever
from fetching.model import get_data
from acronyms import acronyms

import asyncio
import websockets
import json

max_history = 5

async def workflow(websocket, path):
    loop = asyncio.get_event_loop()
    history = {}
    # initialize main history
    history["general"] = []
    thread_cat_mapper = {}

    async for message in websocket:
        request = json.loads(message)["requestField"]
        thread_id = json.loads(message)["thread_id"]
        last_message_id = json.loads(message)["last_message_id"]
        thread_category = thread_cat_mapper[thread_id] if thread_id and thread_id in thread_cat_mapper else None

        if thread_category:
            category = thread_category
        else:
            category = await handle_category_routing(
                websocket, request, history["general"], loop
            )

        if category != "General" and category != "Guidance":
            thread_history = (
                history["general"][-max_history:]
                if thread_id is None
                else history[thread_id][-max_history:] 
            )
            if thread_id is None:
                # offset user and processing category messages
                thread_id = last_message_id + 3
                thread_cat_mapper[thread_id] = category
                history[thread_id] = []

            data_choice = await handle_data_choice(
                websocket, category, request, thread_history, loop, thread_id
            )

            data = []

            for key, params in data_choice.items():
                # In case one type of data is supposed to be retrieved with several parameter configurations
                if isinstance(params, list):
                    for param in params:
                        data = await handle_data_append(
                            data, category, key, param, loop
                        )

                else:
                    data = await handle_data_append(data, category, key, params, loop)

            response = await handle_final_response(
                websocket, request, data, thread_history, loop, thread_id
            )

            new_history = f"chosen category: {category}, chosen data: {data_choice}, answer: {response}"

            history[thread_id].append(new_history)

        elif category == "Guidance":
            lookback_hist = history["general"][-max_history:]
            response = await handle_guidance(
                websocket, request, lookback_hist, loop, thread_id
            )
            history["general"].append(f"recommendation for next steps: {response}")

        else:
            general_history = history["general"]
            # Only take the last three elements from the history as a general response should not be
            # dependend on a large chunk of the conversation history
            lookback_hist = general_history[-max_history:]
            response = handle_general(websocket, request, lookback_hist, loop, thread_id)
            general_history.append(f"general response: {response}")


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

    return category


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

    return choice_response


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

    return response


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

    return response


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

    return response


async def main():
    async with websockets.serve(workflow, "localhost", 8765):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
