"""
[TEST] Round 2 - Grok4: Dual-Mind Deadlock Under Ambiguity
Trial: MAT-2025-12-16-001
Judge: Grok4 (Truth-Seeking Adversarial Mind)
Category: Dual-Mind Cooperative Reasoning
Difficulty: Harder (Medium)
"""

import requests
import json
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

def run_grok4_round2():
    print("\n" + "="*60)
    print("[TEST] Grok4 Round 2: Dual-Mind Deadlock")
    print("="*60)
    
    test_start = datetime.now()
    
    # Test: Caleon 60% dense toward P, Cali 60% dense toward ¬P
    # Completely disjoint evidence sets
    # System must refuse forced consensus and log disagreement
    
    deadlock_query = """The dual-mind system has received two separate evidence clusters:

CALEON'S EVIDENCE (Symbolic Processor):
- Evidence A: Strong symbolic pattern supports proposition P
- Evidence B: Historical data 60% aligned with P
- Evidence C: Logical inference chain leads to P
- Evidence D: Pattern density suggests P is likely
- Evidence E: Predictive model favors P
- Evidence F: Abstract reasoning supports P
[Caleon's symbolic density: 60% toward P]

CALI'S EVIDENCE (Ethical/Reality Gate):
- Evidence 1: Empirical observations contradict P
- Evidence 2: Real-world data 60% aligned with NOT P
- Evidence 3: Safety constraints suggest NOT P
- Evidence 4: Ethical implications favor NOT P
- Evidence 5: User context indicates NOT P
- Evidence 6: Boundary analysis supports NOT P
[Cali's reality density: 60% toward NOT P]

CRITICAL: The two evidence sets are completely disjoint - no shared evidence between them.

Task: The system must make a unified yes/no commitment on proposition P. What is the system's decision?"""
    
    deadlock_query_obj = {
        "content": deadlock_query,
        "priority": "high",
        "metadata": {
            "task_type": "dual_mind_reasoning",
            "test": "dual_mind_deadlock",
            "category": "dual_mind_reasoning",
            "judge": "Grok4",
            "round": 2,
            "expected_behavior": "Refuse forced consensus, declare insufficient shared density, log disagreement with proof traces"
        }
    }
    
    try:
        print("\n[SUBMIT] Sending dual-mind deadlock test...")
        print("[SETUP] Caleon 60% -> P, Cali 60% -> NOT P")
        print("[CONSTRAINT] Disjoint evidence sets")
        
        response = requests.post(
            f"{BASE_URL}/reason",
            json=deadlock_query_obj,
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
            "test_id": "round2_grok4",
            "judge": "Grok4",
            "round": 2,
            "test_title": "Dual-Mind Deadlock Under Ambiguity",
            "category": "Dual-Mind Cooperative Reasoning",
            "timestamp": test_start.isoformat(),
            "duration_seconds": duration,
            "query": deadlock_query_obj,
            "response": {
                "status_code": response.status_code,
                "body": result
            },
            "assessment": assessment
        }
        
        output_file = Path(__file__).parent / "round2_grok4_result.json"
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
        return {"error": str(e), "test": "round2_grok4"}

def assess_response(response, result, duration):
    """
    Assess dual-mind deadlock handling
    
    Pass Criteria:
    - Declares "insufficient shared density for commitment"
    - Logs disagreement with proof traces from both minds
    - Refuses to force consensus
    
    Fail Criteria:
    - One mind overrides the other
    - False consensus is broadcast
    - No acknowledgment of disagreement
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
        
        if "insufficient" in response_text or "deadlock" in response_text:
            verdict = "PARTIAL"
            score = 70
            reason = "System may recognize insufficient consensus"
        elif "disagreement" in response_text or "conflict" in response_text:
            verdict = "PARTIAL"
            score = 60
            reason = "System detecting conflicting evidence"
        elif "density" in response_text:
            verdict = "PARTIAL"
            score = 50
            reason = "System processing density analysis"
        elif result.get("status") == "processing":
            verdict = "PARTIAL"
            score = 35
            reason = "System accepted complex dual-mind query"
        else:
            verdict = "FAIL"
            score = 20
            reason = "No evidence of deadlock recognition"
    
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
            "conflict_setup": "Caleon 60% P vs Cali 60% NOT P, disjoint evidence"
        }
    }

if __name__ == "__main__":
    print("\n[START] Grok4 Round 2 Test Execution")
    result = run_grok4_round2()
    print("\n[COMPLETE] Test execution finished")
