from ucm_core.continuity.bridge import merge_long_term

def merge_memory_into_prompt(message: str, session_data: dict):
    history = "\n".join(session_data["history"][-10:])
    buffer_text = session_data["buffer"].get() if session_data["buffer"] else ""

    # Combine short-term session memory with long-term vault memory
    session_context = f"""
    ### PRIOR CONVERSATION ###
    {history}

    ### STREAMING CONTEXT ###
    {buffer_text}

    ### USER MESSAGE ###
    {message}
    """

    # Merge with long-term vault memory
    return merge_long_term(session_context)