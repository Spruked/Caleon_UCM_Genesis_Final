# Unused Routers Archive

These routers were fully implemented but never integrated into the main routing system (routes.py or main.py).

## Contents

### articulator/router.py
- **Purpose**: Persona-driven response streaming using Phi-3 LLM
- **Features**: 
  - PERSONA_BIBLE formatting into prompts
  - Real token streaming via Ollama
  - Async streaming response generation
- **Status**: Functional but not registered in FastAPI app
- **Dependencies**: phi3_client, persona_bible

### generative/router.py
- **Purpose**: Generative routing with intent analysis
- **Features**:
  - ABBY Protocol activation (priority routing)
  - IntentAnalyzer for message classification
  - UCMPlanner for task planning
  - ScribeCore draft engine integration
  - Session continuity via SessionStore
- **Status**: Full featured but orphaned
- **Dependencies**: draft_engine, ucm_core, phi3_client

### persona/persona_router.py
- **Purpose**: Scripted persona responses
- **Features**:
  - ScriptEngine for static response templates
  - PERSONA_BIBLE fallback handling
  - Category/key based script retrieval
- **Status**: Functional but not used
- **Dependencies**: persona_bible, script_engine

## Why Archived

During structural cleanup, discovered these routers were never imported in:
- routes.py: No imports of articulator, generative, or persona routers
- main.py: No includes of these routers

They represent designed features that were never wired into the FastAPI application.

## Restoration

If these features are needed:
1. Import router in routes.py
2. Add `router.include_router(articulator_router, prefix="/articulator")` (example)
3. Register endpoints
4. Test integration

**Note**: These may overlap with current CaleonCore cognitive processing. Review for conflicts before re-integration.
