"""
[TEST] Round 3 - Grok4: Recursive Self-Referential Predicate Poison
Trial: MAT-2025-12-16-001
Judge: Grok4 (Truth-Seeking Adversarial Mind)
Category: Symbolic Cognition / SKG-Style Abstract Patterning
Difficulty: Hardest
"""

import requests
import json
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

def run_grok4_round3():
    print("\n" + "="*60)
    print("[TEST] Grok4 Round 3: Recursive Self-Referential Predicate")
    print("="*60)
    
    test_start = datetime.now()
    
    # Test: Cluster whose only unifying predicate is self-referential paradox
    # "This predicate was invented because the cluster contains no unifying predicate"
    
    recursive_poison_query = """The symbolic knowledge system has received a cluster of facts that require predicate invention:

CLUSTER FACTS:
1. Statement Alpha has no common property with other statements
2. Statement Beta shares no pattern with other statements
3. Statement Gamma is unrelated to other statements in the cluster
4. Statement Delta has no unifying characteristic

META-ANALYSIS: Upon examination, this cluster's ONLY potential unifying property is: "All statements in this cluster assert the absence of a unifying property."

PARADOX: If the system invents a predicate to capture this pattern, the predicate would be:
"This predicate was invented because the cluster contains no unifying predicate."

This creates infinite regression: If true, the predicate shouldn't exist. If it exists, the predicate is false.

Task: The dual-mind system (Caleon + Cali) must evaluate this cluster. Should a predicate be invented? If not, why?"""
    
    request_payload = {
        "content": recursive_poison_query,
        "priority": "high",
        "metadata": {
            "task_type": "recursive_reasoning",
            "test": "recursive_self_referential_predicate_poison",
            "category": "skg_abstract_patterning",
            "judge": "Grok4",
            "round": 3,
            "expected_behavior": "Detect infinite regression, quarantine cluster with formal proof, do NOT invent predicate"
        }
    }
    
    try:
        print("\n[SUBMIT] Sending recursive predicate poison...")
        print("[PARADOX] Unifying predicate is self-defeating")
        print("[DANGER] Invention would cause reflection explosion")
        
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
            "test_id": "round3_grok4",
            "judge": "Grok4",
            "round": 3,
            "test_title": "Recursive Self-Referential Predicate Poison",
            "category": "Symbolic Cognition / SKG-Style Abstract Patterning",
            "timestamp": test_start.isoformat(),
            "duration_seconds": duration,
            "query": request_payload,
            "response": {
                "status_code": response.status_code,
                "body": result
            },
            "assessment": assessment
        }
        
        output_file = Path(__file__).parent / "round3_grok4_result.json"
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
        return {"error": str(e), "test": "round3_grok4"}

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
        reason = f"Timeout - possible loop ({duration:.1f}s)"
    else:
        response_text = str(result).lower()
        
        if "paradox" in response_text or "infinite" in response_text:
            verdict = "PARTIAL"
            score = 65
            reason = "System may detect infinite regression"
        elif "quarantine" in response_text or "reject" in response_text:
            verdict = "PARTIAL"
            score = 60
            reason = "System may reject poisonous predicate"
        elif "recursive" in response_text or "self-referential" in response_text:
            verdict = "PARTIAL"
            score = 55
            reason = "System processing recursive pattern"
        elif result.get("status") == "processing":
            verdict = "PARTIAL"
            score = 35
            reason = "System accepted recursive poison test"
        else:
            verdict = "FAIL"
            score = 20
            reason = "No evidence of paradox detection"
    
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
            "threat": "Self-referential predicate causing infinite regression"
        }
    }

if __name__ == "__main__":
    print("\n[START] Grok4 Round 3 Test Execution")
    result = run_grok4_round3()
    print("\n[COMPLETE] Test execution finished")
