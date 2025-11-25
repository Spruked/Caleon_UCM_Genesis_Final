from ucm_core.vault.vault_core import vault

def merge_long_term(session_input: str):
    context = vault.gather_context()

    merged = f"""
    ## A PRIORI TRUTHS ##
    {context['a_priori']}

    ## IDENTITY THREADS ##
    {context['identity']}

    ## ETHICAL RULES ##
    {context['ethics']}

    ## LEARNED FACTS ##
    {context['learned']}

    ## USER PREFERENCES ##
    {context['preferences']}

    ## EVENTS ##
    {context['events']}

    ## USER INPUT ##
    {session_input}
    """

    return merged