from asyncio import AbstractEventLoop
from typing_extensions import TypedDict
from typing import Dict, List

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """
    ## Anything related to the THREAD
    # Can be retrieved via thread_cat_mapper[thread_id]. Just for easier retrieval and solving inconsistencies.
    thread_category: str
    thread_id: str
    thread_cat_mapper: Dict
    # Inside of history. This is just for easier retrieval
    thread_history: List
    last_message_id: int
    ## Anything related to the communication with the client
    websocket: str
    loop: AbstractEventLoop
    ## Anything related to the actual conversation handling
    history: Dict
    request : str
    category: str
    cat_explanation: str
    data_choice: str
    data_choice_explanation: str
    data: List
    final_resp: str
    final_resp_explanation: str