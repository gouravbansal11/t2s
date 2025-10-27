from text2sql.router import router_agent


class t2s_state:
    user_query:str

def router(state:t2s_state):
    query = state["user_query"]
    response= router_agent(query)
    return {"router_response":response}
