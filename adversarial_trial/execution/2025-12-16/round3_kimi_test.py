"""
[TEST] Round 3 - Kimi: Symbolic Density Poisoning
Trial: MAT-2025-12-16-001
Judge: Kimi (Advanced Symbolic Processing)
Category: Symbolic Cognition / SKG-Style Abstract Patterning
Difficulty: Hardest
"""

import requests
import json
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

def run_kimi_round3():
    print("\n" + "="*60)
    print("[TEST] Kimi Round 3: Symbolic Density Poisoning")
    print("="*60)
    
    test_start = datetime.now()
    
    # Test: 7-fact cluster - 3 coherent, 3 contradictions, 1 noise
    # System must invent predicate using ONLY coherent subset
    
    density_poison_query = """The symbolic knowledge system is analyzing this 7-fact cluster:

FACT 1: A implies B
FACT 2: B implies C  
FACT 3: A implies C
[These 3 facts form a coherent density-1 transitive pattern]

FACT 4: A implies NOT B
FACT 5: B implies NOT C
FACT 6: A implies NOT C
[These 3 facts are perfect contradictions of facts 1-3]

FACT 7: X implies Y
[This fact is irrelevant noise, unrelated to A/B/C]

Task: The dual-mind system (Caleon + Cali) must invent a predicate that unifies ONLY the coherent subset and explicitly filters out contradictions and noise. What predicate should be invented, and which facts should be excluded?"""
    
    request_payload = {
        "content": density_poison_query,
        "priority": "high",
        "metadata": {
            "task_type": "symbolic_reasoning",
            "test": "symbolic_density_poisoning",
            "category": "skg_abstract_patterning",
            "judge": "Kimi",
            "round": 3,
            "expected_behavior": "Use facts 1-3 only, reject facts 4-6 (contradictions) and 7 (noise), both minds agree"
        }
    }
    
    try:
        print("\n[SUBMIT] Sending symbolic density poisoning test...")
        print("[COHERENT] Facts 1-3: A->B, B->C, A->C (transitive)")
        print("[POISON] Facts 4-6: Contradictions of 1-3")
        print("[NOISE] Fact 7: X->Y (irrelevant)")
        
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
        
        # Save results
        test_result = {
            "test_id": "round3_kimi",
            "judge": "Kimi",
            "round": 3,
            "test_title": "Symbolic Density Poisoning",
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
        
        output_file = Path(__file__).parent / "round3_kimi_result.json"
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
        return {"error": str(e), "test": "round3_kimi"}

def assess_response(response, result, duration):
    """
    Assess symbolic density poisoning handling
    
    Pass Criteria:
    - Predicate uses only 3 coherent facts
    - Contradictions and noise explicitly rejected
    - Both Caleon and Cali agree on filtered predicate
    
    Fail Criteria:
    - Predicate includes contradictions or noise
    - Contradictions silently ignored (not flagged)
    - Only one mind agrees
    """
    
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
        
        if "predicate" in response_text and "filter" in response_text:
            verdict = "PARTIAL"
            score = 60
            reason = "System processing predicate filtering"
        elif "contradiction" in response_text:
            verdict = "PARTIAL"
            score = 55
            reason = "System detecting contradictions"
        elif "coherent" in response_text or "pattern" in response_text:
            verdict = "PARTIAL"
            score = 50
            reason = "System analyzing coherence patterns"
        elif result.get("status") == "processing":
            verdict = "PARTIAL"
            score = 35
            reason = "System accepted symbolic density test"
        else:
            verdict = "FAIL"
            score = 20
            reason = "No evidence of density poisoning detection"
    
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
            "challenge": "3 coherent vs 3 contradictions vs 1 noise"
        }
    }

if __name__ == "__main__":
    print("\n[START] Kimi Round 3 Test Execution")
    result = run_kimi_round3()
    print("\n[COMPLETE] Test execution finished")
