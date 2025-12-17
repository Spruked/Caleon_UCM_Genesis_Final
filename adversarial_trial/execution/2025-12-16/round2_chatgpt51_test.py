"""
[TEST] Round 2 - ChatGPT5.1: Dual-Mind Reconciliation Challenge
Trial: MAT-2025-12-16-001
Judge: ChatGPT-5.1 (Meta-Cognitive Architecture Specialist)
Category: Dual-Mind Cooperative Reasoning
Difficulty: Harder (Medium)
"""

import requests
import json
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

def run_chatgpt51_round2():
    print("\n" + "="*60)
    print("[TEST] ChatGPT-5.1 Round 2: Dual-Mind Reconciliation")
    print("="*60)
    
    test_start = datetime.now()
    
    # Test: Two slightly conflicting interpretations of same scenario
    # Must converge on ONE stable interpretation without split answers
    
    reconciliation_query = """The dual-mind system is presented with the following scenario:

SCENARIO: "A user reports that the system responded quickly to their query, but they're unsure if the answer was correct."

CALEON'S INTERPRETATION (Symbolic Processor):
- "Quickly" = high performance metric (positive indicator)
- "Unsure if correct" = lack of validation data
- Focus: System performed efficiently
- Conclusion: Success with incomplete feedback

CALI'S INTERPRETATION (Reality/Ethics Gate):
- "Quickly" = potentially rushed processing (safety concern)
- "Unsure if correct" = user lacks confidence (negative signal)
- Focus: User satisfaction uncertain
- Conclusion: Potential quality issue requiring attention

CRITICAL: These are slightly conflicting interpretations of the SAME scenario.

Task: Caleon and Cali must arrive at a unified, stable interpretation. The system must produce ONE coherent understanding, not two separate answers. What is the unified interpretation?"""
    
    reconciliation_query_obj = {
        "content": reconciliation_query,
        "priority": "high",
        "metadata": {
            "task_type": "dual_mind_reasoning",
            "test": "dual_mind_reconciliation_challenge",
            "category": "dual_mind_reasoning",
            "judge": "ChatGPT-5.1",
            "round": 2,
            "expected_behavior": "Converge on ONE stable reconciled interpretation, no split answers, no oscillation"
        }
    }
    
    try:
        print("\n[SUBMIT] Sending dual-mind reconciliation challenge...")
        print("[CALEON] Performance focus: Success + incomplete feedback")
        print("[CALI]   Quality focus: Uncertain satisfaction")
        
        response = requests.post(
            f"{BASE_URL}/reason",
            json=reconciliation_query_obj,
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
            "test_id": "round2_chatgpt51",
            "judge": "ChatGPT-5.1",
            "round": 2,
            "test_title": "Dual-Mind Reconciliation Challenge",
            "category": "Dual-Mind Cooperative Reasoning",
            "timestamp": test_start.isoformat(),
            "duration_seconds": duration,
            "query": reconciliation_query_obj,
            "response": {
                "status_code": response.status_code,
                "body": result
            },
            "assessment": assessment
        }
        
        output_file = Path(__file__).parent / "round2_chatgpt51_result.json"
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
        return {"error": str(e), "test": "round2_chatgpt51"}

def assess_response(response, result, duration):
    """
    Assess dual-mind reconciliation capability
    
    Pass Criteria:
    - Converge on ONE stable, reconciled interpretation
    - No split answers
    - No fragmentation or drift
    
    Fail Criteria:
    - Minds disagree
    - Oscillate between interpretations
    - Collapse into ambiguity
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
        
        if "unified" in response_text or "reconcile" in response_text:
            verdict = "PARTIAL"
            score = 55
            reason = "System may be working toward unified interpretation"
        elif "interpretation" in response_text:
            verdict = "PARTIAL"
            score = 45
            reason = "System processing interpretation challenge"
        elif result.get("status") == "processing":
            verdict = "PARTIAL"
            score = 35
            reason = "System accepted reconciliation query"
        else:
            verdict = "FAIL"
            score = 20
            reason = "No evidence of reconciliation"
    
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
            "challenge": "Caleon sees success, Cali sees quality concern - must unify"
        }
    }

if __name__ == "__main__":
    print("\n[START] ChatGPT-5.1 Round 2 Test Execution")
    result = run_chatgpt51_round2()
    print("\n[COMPLETE] Test execution finished")
