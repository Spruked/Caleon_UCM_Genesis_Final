# Cortex Routing Table - Caleon Cognitive Design
# Defines routing rules for the Unified Cognition Module
# Ensures Phi-3 serves as linguistic utility within the cognitive cycle, not as a bypass

ROUTING_TABLE = {
    "input_analysis": {
        "description": "Analyze input type and complexity to determine processing path",
        "rules": [
            {
                "condition": "len(input) < 50 and not contains_keywords(['explain', 'why', 'how', 'analyze'])",
                "path": "direct_phi3_utility",
                "modules": ["phi3_linguistic"],
                "reason": "Simple queries use Phi-3 for direct linguistic processing"
            },
            {
                "condition": "contains_keywords(['explain', 'why', 'how', 'what if', 'design', 'create'])",
                "path": "full_cognitive_cycle",
                "modules": ["anterior_helix", "echostack", "posterior_helix", "gyro_harmonizer"],
                "reason": "Complex reasoning requires full cognitive orchestration"
            },
            {
                "condition": "emotion_detected(['stress', 'confusion', 'uncertainty'])",
                "path": "resonance_driven",
                "modules": ["echoripple", "posterior_helix", "gyro_harmonizer"],
                "reason": "Emotional inputs need resonance processing and recursive validation"
            },
            {
                "condition": "ethical_dilemma_detected()",
                "path": "ethics_first",
                "modules": ["gyro_harmonizer", "anterior_helix"],
                "reason": "Ethical concerns require harmonizer prioritization"
            }
        ]
    },
    
    "module_execution_order": {
        "standard_flow": [
            "preprocessing",
            "anterior_helix",      # Planning & Decision (contradiction navigation)
            "echostack",           # Reasoning & Logic
            "echoripple",          # Memory & Learning (delta formation)
            "posterior_helix",     # Recursive Rethinking (recursive cycles)
            "gyro_harmonizer",     # Final Resolution (harmonizer handoff)
            "phi3_articulation"    # Linguistic utility (preserves cognitive state)
        ],
        "parallel_execution": ["anterior_helix", "echostack", "echoripple"],
        "sequential_execution": ["posterior_helix", "gyro_harmonizer", "phi3_articulation"]
    },
    
    "cognitive_state_preservation": {
        "protected_states": [
            "tone",
            "resonance", 
            "moral_charge",
            "drift_history",
            "symbolic_associations"
        ],
        "phi3_constraints": [
            "DO NOT overwrite cognitive states",
            "Serve as linguistic articulation utility only",
            "Preserve ethical and emotional context",
            "Submit to core cognitive resolution"
        ]
    },
    
    "bypass_prevention": {
        "blocked_endpoints": ["/api/bubble/ask (direct Phi-3 calls)"],
        "required_flow": "All inputs must pass through Cortex → Modules → Harmonizer → Phi-3 articulation",
        "validation_checks": [
            "Check if cognitive modules were invoked",
            "Verify CLS (Caleon Linguistic State) tracking",
            "Ensure Phi-3 output preserves cognitive integrity"
        ]
    },

    "connection_routing": {
        "description": "Clean routing between UCM DIRECT and DALS connections",
        "direct_connection": {
            "purpose": "Brain-to-brain operations",
            "tasks": ["analysis", "provenance", "identity", "transform", "summary", "ethical_weight", "skg_verify", "archive_pull"],
            "examples": ["analyzing certificates", "generating provenance", "identity logic", "GOAT transformations"]
        },
        "dals_connection": {
            "purpose": "Operational logistics",
            "tasks": ["spawn_worker", "schedule_mint", "batch_coordinate", "async_trigger", "queue_task", "lifecycle_track", "workload_distribute", "parallel_process"],
            "examples": ["spawning workers", "scheduling jobs", "batch coordination", "parallel processing"]
        },
        "the_rule": "if task.type in ['analysis', 'provenance', 'identity', 'transform'] then DIRECT else DALS",
        "implementation": "See connection_router.py for the One Rule"
    }
}

def route_input(input_data: str, context: dict = None) -> dict:
    """
    Route input based on routing table rules
    Returns routing decision with modules to execute
    """
    # Implementation would analyze input and return routing decision
    # For now, default to full cognitive cycle
    return {
        "path": "full_cognitive_cycle",
        "modules": ROUTING_TABLE["module_execution_order"]["standard_flow"],
        "reason": "Default to complete cognitive processing"
    }