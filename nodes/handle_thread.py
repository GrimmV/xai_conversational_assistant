from config import max_hist

def handle_thread(state):
    
    history = state["history"]
    thread_id = state["thread_id"] if "thread_id" in state else None
    thread_cat_mapper = state["thread_cat_mapper"]
    last_message_id = state["last_message_id"]
    thread_category = state["thread_category"]
    
    thread_history = (
        history["general"][-max_hist:]
        if thread_id is None
        else history[thread_id][-max_hist:] 
    )
    if thread_id is None:
        # offset user and processing category messages
        thread_id = last_message_id + 3
        thread_cat_mapper[thread_id] = thread_category
        history[thread_id] = []
        
    state["thread_history"] = thread_history
    state["history"] = history
    print(state["history"])
    state["thread_id"] = thread_id
    state["thread_cat_mapper"] = thread_cat_mapper
    
    print("#####")
    print(state)
    
    return state