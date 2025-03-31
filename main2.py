from state.GraphState import GraphState

from state_workflow import get_workflow

import asyncio
import websockets
import json

async def workflow(websocket, path):
    print("I am here")
    loop = asyncio.get_event_loop()
    history = {}
    # initialize main history
    history["general"] = []
    thread_cat_mapper = {}
    initial_state = {
        "loop": loop,
        "history": history,
        "thread_cat_mapper": thread_cat_mapper, 
        "websocket": websocket              
    }
    
    my_thread_id = 0

    async for message in websocket:
        
        request = json.loads(message)["requestField"]
        thread_id = json.loads(message)["thread_id"]
        last_message_id = json.loads(message)["last_message_id"]
        thread_category = thread_cat_mapper[thread_id] if thread_id and thread_id in thread_cat_mapper else None
        
        initial_state["request"] = request
        initial_state["last_message_id"] = last_message_id
        initial_state["thread_category"] = thread_category
        
        app = get_workflow()
        my_thread_id = my_thread_id + 1
        async for output in app.astream(initial_state, config={"configurable": {"thread_id": my_thread_id}}):
            print(output)
        

async def main():
    async with websockets.serve(workflow, "localhost", 8765):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
