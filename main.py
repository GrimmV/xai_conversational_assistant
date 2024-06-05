from CategoryRoutingBot import CategoryRoutingBot
from CategoryBot import CategoryBot
from GeneralBot import GeneralBot
from ResponseBot import ResponseBot
from ExplanationRetriever import ExplanationRetriever
from fetching.model import get_data

import asyncio
import websockets
import json

async def workflow(websocket, path):
    loop = asyncio.get_event_loop()

    async for message in websocket:
        request = json.loads(message)["requestField"]
        await websocket.send(json.dumps({
            "type": "status",
            "text": "Choosing category..."
        }))
        explanation_retriever = ExplanationRetriever()
        category_router = CategoryRoutingBot()

        routing_response = await loop.run_in_executor(None, category_router.handle_request, request)
        category = routing_response["category"]
        category_explanation = routing_response["explanation"]
        await websocket.send(json.dumps({
            "type": "routing",
            "category": category,
            "explanation": category_explanation
        }))
        
        if category != "General":
            await websocket.send(json.dumps({
                "type": "status",
                "text": "Looking for relevant data..."
            }))
            category_bot = CategoryBot(category)
            data_choice = await loop.run_in_executor(None, category_bot.handle_request, request)
            choice_response = data_choice["response"]
            choice_explanation = data_choice["explanation"]
            await websocket.send(json.dumps({
                "type": "data_choice",
                "choice": json.dumps(choice_response),
                "explanation": json.dumps(choice_explanation)
            }))

            data = []

            for key, params in data_choice["response"].items():
                data.append(
                    {
                        "data": await loop.run_in_executor(None, get_data, category.lower(), key, params),
                        "explanation": await loop.run_in_executor(None, explanation_retriever.get_explanation, key),
                    }
                )

            await websocket.send(json.dumps({
                "type": "status",
                "text": "Produce final response..."
            }))
            response_bot = ResponseBot()
            final_response = await loop.run_in_executor(None, response_bot.handle_request, request, data)

            response = final_response["response"]
            explanation = final_response["explanation"]
            what_next = final_response["next"]

            await websocket.send(json.dumps({
                "type": "response",
                "response": response,
                "explanation": explanation,
                "next": what_next
            }))
        else:
            general_bot = GeneralBot()
            general_response = await loop.run_in_executor(None, general_bot.handle_request(request))
            await websocket.send({
                "type": "response",
                "response": general_response["response"],
                "explanation": general_response["explanation"]
            })


def get_data_choice_bot(category):
    if category == "General":
        return GeneralBot()
    else:
        return CategoryBot(category)


async def main():
    async with websockets.serve(workflow, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())