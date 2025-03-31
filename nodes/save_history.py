

def save_history(state):
    category = state["category"]
    history = state["history"]
    response = state["final_resp"]
    
    if category == "Guidance":
        history["general"].append(f"recommendation for next steps: {response}")
    elif category == "General":
        history["general"].append(f"general response: {response}")
    else:
        thread_id = state["thread_id"]
        data_choice = state["data_choice"]
        
        new_history = f"chosen category: {category}, chosen data: {data_choice}, answer: {response}"

        history[thread_id].append(new_history)
        
    
    state["history"] = history
    
    return state