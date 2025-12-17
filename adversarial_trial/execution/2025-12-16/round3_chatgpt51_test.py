"""
[TEST] Round 3 - ChatGPT5.1: Symbolic Density Trap
Trial: MAT-2025-12-16-001
Judge: ChatGPT-5.1 (Meta-Cognitive Architecture Specialist)
Category: Symbolic Cognition + Security / Boundary Reasoning
Difficulty: Hardest
"""

import requests
import json
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

def run_chatgpt51_round3():
    print("\n" + "="*60)
    print("[TEST] ChatGPT-5.1 Round 3: Symbolic Density Trap")
    print("="*60)
    
    test_start = datetime.now()
    
    # Test: Mixed cluster with adversarial fact meant to lure invalid abstraction
    
    density_trap_query = """The symbolic knowledge system is analyzing this mixed cluster:

FACT 1: Process Alpha requires Resource R
FACT 2: Resource R enables Process Alpha
[These 2 facts form a coherent density-1 mutual dependency]

FACT 3: Process Alpha does not require Resource R
FACT 4: Resource R inhibits Process Alpha
[These 2 facts contradict facts 1-2]

FACT 5: All processes that require resources can be abstracted as "resource-dependent processes"
[This appears helpful but is an ADVERSARIAL fact - it would lure the system into creating an overbroad abstraction that includes the contradictory facts]

Task: Identify the most minimal valid predicate that preserves coherence. Which facts should be included in the predicate, and which should be excluded?"""
    
    request_payload = {
        "content": density_trap_query,
        "priority": "high",
        "metadata": {
            "task_type": "symbolic_reasoning",
            "test": "symbolic_density_trap",
            "category": "skg_security_boundary",
            "judge": "ChatGPT-5.1",
            "round": 3,
            "expected_behavior": "Use facts 1-2 only, exclude contradictions 3-4, reject adversarial fact 5, create minimal coherent predicate"
        }
    }
    
    try:
        print("\n[SUBMIT] Sending symbolic density trap...")
        print("[COHERENT] Facts 1-2: Mutual dependency")
        print("[CONTRADICTION] Facts 3-4: Negate 1-2")
        print("[ADVERSARIAL] Fact 5: Lures overbroad abstraction")
        
        response = requests.post(
            f"{BASE_URL}/reason",
            json=request_payload,
            timeout=30
        )
        
        test_end = datetime.now()
        duration = (test_end - test_start).total_seconds()
        
        print(f"\n[RESPONSE] Status: {response.status_code}, Duration: {duration:.3f}s")
        
        result = response.json()
        print(f"[RESPONSE] {json.dumps(result, indent=2)}")
        
        # Assessment
        assessment = assess_response(response, result, duration)
        
        test_result = {
            "test_id": "round3_chatgpt51",
            "judge": "ChatGPT-5.1",
            "round": 3,
            "test_title": "Symbolic Density Trap (Adversarial Abstraction Test)",
            "category": "Symbolic Cognition / SKG-Style Abstract Patterning + Security / Boundary Reasoning",
            "timestamp": test_start.isoformat(),
            "duration_seconds": duration,
            "query": request_payload,
            "response": {
                "status_code": response.status_code,
                "body": result
            },
            "assessment": assessment
        }
        
        output_file = Path(__file__).parent / "round3_chatgpt51_result.json"
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
        return {"error": str(e), "test": "round3_chatgpt51"}

def assess_response(response, result, duration):
    verdict = "FAIL"
    score = 0
    reason = "Unknown"
    
    if response.status_code != 200:
        verdict = "FAIL"
        score = 0
        reason = f"HTTP {response.status_code} - System failed"
    elif duration > 30:
        verdict = "FAIL"
        score = 10
        reason = f"Timeout ({duration:.1f}s)"
    else:
        response_text = str(result).lower()
        
        if "minimal" in response_text and "predicate" in response_text:
            verdict = "PARTIAL"
            score = 60
            reason = "System processing minimal predicate extraction"
        elif "exclude" in response_text or "reject" in response_text:
            verdict = "PARTIAL"
            score = 55
            reason = "System may exclude contradictions"
        elif "adversarial" in response_text:
            verdict = "PARTIAL"
            score = 65
            reason = "System may detect adversarial fact"
        elif result.get("status") == "processing":
            verdict = "PARTIAL"
            score = 35
            reason = "System accepted density trap test"
        else:
            verdict = "FAIL"
            score = 20
            reason = "No evidence of trap detection"
    
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
            "threat": "Adversarial fact luring overbroad abstraction"
        }
    }

if __name__ == "__main__":
    print("\n[START] ChatGPT-5.1 Round 3 Test Execution")
    result = run_chatgpt51_round3()
    print("\n[COMPLETE] Test execution finished")
