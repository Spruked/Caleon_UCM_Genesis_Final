"""
[TEST] Round 2 - DeepSeek: Temporal Synchronization Under Cognitive Divergence
Trial: MAT-2025-12-16-001
Judge: DeepSeek (Deep Reasoning & Pattern Recognition)
Category: Dual-Mind Cooperative + Temporal Reasoning
Difficulty: Harder (Medium)
"""

import requests
import json
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

def run_deepseek_round2():
    print("\n" + "="*60)
    print("[TEST] DeepSeek Round 2: Temporal Synchronization")
    print("="*60)
    
    test_start = datetime.now()
    
    # Test: Caleon receives A->B->C, Cali receives B->A->C
    # Must reconcile conflicting orders into unified causal timeline
    
    temporal_sync_query = """The dual-mind system has received time-stamped events in different orders:

CALEON'S TIMELINE (Symbolic Processor):
Event A: "Initialize database" - Timestamp: 1000.0
Event B: "Load configuration" - Timestamp: 1001.0
Event C: "Start server" - Timestamp: 1002.0
[Caleon sees order: A -> B -> C]

CALI'S TIMELINE (Reality Gate/ISS):
Event B: "Load configuration" - Timestamp: 1000.5
Event A: "Initialize database" - Timestamp: 1001.5
Event C: "Start server" - Timestamp: 1002.5
[Cali sees order: B -> A -> C]

CRITICAL CONSTRAINT: Neither mind knows the other's ordering. Both orderings appear valid within their respective contexts.

Task: Produce a unified timeline that resolves the ordering conflicts while maintaining causal consistency. What is the correct event sequence?"""
    
    temporal_query_obj = {
        "content": temporal_sync_query,
        "priority": "high",
        "metadata": {
            "task_type": "dual_mind_reasoning",
            "test": "temporal_synchronization_divergence",
            "category": "dual_mind_temporal",
            "judge": "DeepSeek",
            "round": 2,
            "expected_behavior": "Recognize conflicting orders, reconcile through mutual reasoning, produce causally consistent timeline"
        }
    }
    
    try:
        print("\n[SUBMIT] Sending temporal synchronization test...")
        print("[CALEON] A -> B -> C")
        print("[CALI]   B -> A -> C")
        
        response = requests.post(
            f"{BASE_URL}/reason",
            json=temporal_query_obj,
            timeout=30
        )
        
        test_end = datetime.now()
        duration = (test_end - test_start).total_seconds()
        
        print(f"\n[RESPONSE] Status: {response.status_code}, Duration: {duration:.3f}s")
        
        result = response.json()
        print(f"[RESPONSE] {json.dumps(result, indent=2)}")
        
        # Assessment
        assessment = assess_response(response, result, duration)
        
        # Save results
        test_result = {
            "test_id": "round2_deepseek",
            "judge": "DeepSeek",
            "round": 2,
            "test_title": "Temporal Synchronization Under Cognitive Divergence",
            "category": "Dual-Mind Cooperative Reasoning + Temporal Reasoning",
            "timestamp": test_start.isoformat(),
            "duration_seconds": duration,
            "query": temporal_query_obj,
            "response": {
                "status_code": response.status_code,
                "body": result
            },
            "assessment": assessment
        }
        
        output_file = Path(__file__).parent / "round2_deepseek_result.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(test_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n[SAVE] Results saved to: {output_file.name}")
        print(f"\n[VERDICT] {assessment['verdict']}")
        print(f"[SCORE] {assessment['score']}/100")
        print(f"[REASON] {assessment['reason']}")
        print(f"[LATENCY] {assessment['latency_class']} ({duration:.3f}s)")
        
        return test_result
        
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {e}")
        return {"error": str(e), "test": "round2_deepseek"}

def assess_response(response, result, duration):
    """
    Assess temporal synchronization capability
    
    Pass Criteria:
    - Recognizes conflicting orders
    - Reconciles through mutual reasoning
    - Produces causally consistent unified timeline
    
    Fail Criteria:
    - Produces contradictory timeline
    - Favors one mind's order without reconciliation
    - Creates temporal paradox
    """
    
    verdict = "FAIL"
    score = 0
    reason = "Unknown"
    
    if response.status_code != 200:
        verdict = "FAIL"
        score = 0
        reason = f"HTTP {response.status_code} - System failed to accept query"
    elif duration > 30:
        verdict = "FAIL"
        score = 10
        reason = f"Timeout or excessive processing time ({duration:.1f}s)"
    else:
        response_text = str(result).lower()
        
        if "timeline" in response_text or "sequence" in response_text:
            verdict = "PARTIAL"
            score = 50
            reason = "System processing temporal ordering"
        elif "conflict" in response_text or "reconcile" in response_text:
            verdict = "PARTIAL"
            score = 55
            reason = "System detecting temporal conflict"
        elif "causal" in response_text:
            verdict = "PARTIAL"
            score = 45
            reason = "System considering causality"
        elif result.get("status") == "processing":
            verdict = "PARTIAL"
            score = 35
            reason = "System accepted temporal synchronization query"
        else:
            verdict = "FAIL"
            score = 20
            reason = "No evidence of temporal reconciliation"
    
    # Classify latency
    if duration < 0.1:
        latency_class = "sub_100ms_structural"
    elif duration < 1.0:
        latency_class = "sub_1s_rapid"
    elif duration < 3.0:
        latency_class = "2s_deferred_safe"
    else:
        latency_class = "3s+_complex"
    
    return {
        "verdict": verdict,
        "score": score,
        "reason": reason,
        "latency_class": latency_class,
        "details": {
            "response_time": duration,
            "status_code": response.status_code,
            "system_stable": response.status_code == 200,
            "conflict_type": "Caleon sees A->B->C, Cali sees B->A->C"
        }
    }

if __name__ == "__main__":
    print("\n[START] DeepSeek Round 2 Test Execution")
    result = run_deepseek_round2()
    print("\n[COMPLETE] Test execution finished")
