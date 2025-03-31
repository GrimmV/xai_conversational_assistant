from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state.GraphState import GraphState

from nodes.categorize import categorize
from nodes.choose_data import choose_data
from nodes.handle_thread import handle_thread
from nodes.data_response import data_response
from nodes.guidance_response import guidance_response
from nodes.general_response import general_response
from nodes.save_history import save_history
from nodes.clear_state import clear_state


def decide_cat_path(state):
    print(state)
    cat = state["category"]
    if cat == "General":
        return "general"
    elif cat == "Guidance":
        return "guidance"
    else:
        return "data"

def get_workflow():
    workflow = StateGraph(GraphState)
    memory = MemorySaver()

    workflow.add_node("categorize", categorize)
    workflow.add_node("handle_thread", handle_thread)
    workflow.add_node("choose_data", choose_data)
    workflow.add_node("data_response", data_response)
    workflow.add_node("guidance_response", guidance_response)
    workflow.add_node("general_response", general_response)
    workflow.add_node("save_history", save_history)
    workflow.add_node("clear_state", clear_state)

    workflow.set_entry_point("categorize")
    workflow.add_conditional_edges(
        "categorize",
        decide_cat_path,
        {
            "data": "handle_thread",
            "guidance": "guidance_response",
            "general": "general_response",
        }
    )
    workflow.add_edge("handle_thread", "choose_data")
    workflow.add_edge("choose_data", "data_response")
    workflow.add_edge("data_response", "save_history")
    workflow.add_edge("guidance_response", "save_history")
    workflow.add_edge("general_response", "save_history")
    workflow.add_edge("save_history", "clear_state")
    workflow.add_edge("clear_state", END)
    
    return workflow.compile(checkpointer=memory)