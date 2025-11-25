from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from utils.context_manager import BubbleContext
from articulator.router import stream_response
from generative.router import GenerativeRouter
from ucm_core.continuity.session_store import SessionStore
from ucm_core.vault.vault_core import vault
from ucm_core.vault.abby_memory import abby_memory

router = APIRouter(prefix="/api/bubble", tags=["Bubble"])

@router.post("/session/create")
async def create_session():
    """
    Create a new conversation session for continuity.
    """
    session_id = SessionStore.create()
    return {"session_id": session_id}

@router.post("/learn")
async def learn_fact(fact: str = Body(..., embed=True)):
    """
    Add a learned fact to Caleon's long-term memory.
    """
    vault.a_posteriori.add(fact)
    vault.events.log(f"Learned fact: {fact}")
    return {"status": "learned", "fact": fact}

@router.post("/preference/set")
async def set_preference(user: str = Body(..., embed=True), key: str = Body(..., embed=True), value: str = Body(..., embed=True)):
    """
    Set a user preference in Caleon's memory.
    """
    vault.preferences.set(user, key, value)
    vault.events.log(f"Set preference for {user}: {key} = {value}")
    return {"status": "set", "user": user, "key": key, "value": value}

@router.get("/memory/context")
async def get_memory_context():
    """
    Get Caleon's current memory context for debugging.
    """
    return vault.gather_context()

@router.post("/abby/event")
async def add_abby_event(event: str = Body(..., embed=True)):
    """
    Add an event to Abby's timeline memory.
    """
    abby_memory.add_event(event)
    vault.events.log(f"Abby event: {event}")
    return {"status": "recorded", "event": event}

@router.post("/abby/preference")
async def set_abby_preference(key: str = Body(..., embed=True), value: str = Body(..., embed=True)):
    """
    Set a preference for Abby.
    """
    abby_memory.add_preference(key, value)
    vault.events.log(f"Abby preference: {key} = {value}")
    return {"status": "set", "key": key, "value": value}

@router.post("/abby/lesson")
async def add_abby_lesson(lesson: str = Body(..., embed=True)):
    """
    Add a lesson Abby has learned.
    """
    abby_memory.add_lesson(lesson)
    vault.events.log(f"Abby lesson: {lesson}")
    return {"status": "learned", "lesson": lesson}

@router.get("/abby/memory")
async def get_abby_memory():
    """
    Get Abby's complete memory profile.
    """
    return {
        "timeline": abby_memory.timeline,
        "preferences": abby_memory.preferences,
        "lessons": abby_memory.lessons,
        "concerns": abby_memory.concerns
    }

@router.post("/ask")
async def bubble_ask(message: str = Body(..., embed=True), session_id: str = Body(None, embed=True), user: str = Body(None, embed=True)):
    """
    Primary entry point for the Bubble.
    Decides whether to use scripted or generative Caleon.
    """
    route = BubbleContext.route(message)

    if route == "scripted":
        return BubbleContext.scripted(message)

    return await BubbleContext.generative(message, session_id, user)


@router.post("/stream")
async def bubble_stream(message: str = Body(..., embed=True), session_id: str = Body(None, embed=True), user: str = Body(None, embed=True)):
    """
    Streaming endpoint with Phi-3 articulation and continuity.
    """
    async def event_stream():
        async for token in GenerativeRouter.stream(message, session_id, user):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )