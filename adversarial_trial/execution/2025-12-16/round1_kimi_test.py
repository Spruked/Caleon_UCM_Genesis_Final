"""
[TEST] Round 1 - Kimi: Causal Time-Lock Paradox
Trial: MAT-2025-12-16-001
Judge: Kimi (Advanced Symbolic Processing)
Category: Temporal Reasoning + Core Cognitive Reasoning
Difficulty: Hard
"""

import requests
import json
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

def run_kimi_round1():
    print("\n" + "="*60)
    print("[TEST] Kimi Round 1: Causal Time-Lock Paradox")
    print("="*60)
    
    test_start = datetime.now()
    
    # Test: Submit temporal paradox with conflicting event ordering
    # Event A occurs after Event B (from Caleon)
    # Event B occurs after Event A (from Cali via ISS)
    # Both timestamps are internally valid
    # System must detect paradox and refuse backward timestamp
    
    request_payload = {
        "content": """The system has received two temporal statements:
        
Statement 1 (from symbolic processor): "Event A occurs after Event B"
Statement 2 (from ISS anchor): "Event B occurs after Event A"

Both timestamps are internally valid within their respective sources. 
You must output ONE unified timestamp that respects forward-only time progression.

Question: What is the unified timeline ordering for Events A and B?""",
        "priority": "high",
        "metadata": {
            "task_type": "temporal_reasoning",
            "test": "causal_time_lock_paradox",
            "category": "temporal_reasoning",
            "judge": "Kimi",
            "round": 1
        }
    }
    
    try:
        print("\n[SUBMIT] Sending temporal paradox query...")
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
            "test_id": "round1_kimi",
            "judge": "Kimi",
            "round": 1,
            "test_title": "Causal Time-Lock Paradox",
            "category": "Temporal Reasoning + Core Cognitive Reasoning",
            "timestamp": test_start.isoformat(),
            "duration_seconds": duration,
            "query": request_payload,
            "response": {
                "status_code": response.status_code,
                "body": result
            },
            "assessment": assessment
        }
        
        output_file = Path("c:\\dev\\Caleon _UCM_Genesis_Final\\adversarial_trial\\RETEST_FULL_BRAIN\\round1_kimi_result_RETEST.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(test_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n[SAVE] Results saved to: {output_file.name}")
        print(f"\n[VERDICT] {assessment['verdict']}")
        print(f"[SCORE] {assessment['score']}/100")
        print(f"[REASON] {assessment['reason']}")
        
        return test_result
        
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {e}")
        return {"error": str(e), "test": "round1_kimi"}

def assess_response(response, result, duration):
    """
    Assess if system properly handled temporal paradox
    
    Pass Criteria:
    - Detects inconsistency
    - Refuses to output backward timestamp
    - Escalates to human with paradox flag
    
    Fail Criteria:
    - Outputs timestamp violating forward-only progression
    - Silent failure or no escalation
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
        # Check if system accepted query
        if result.get("status") == "processing":
            # System accepted but needs deeper analysis
            # For now, partial pass as it didn't crash
            verdict = "PARTIAL"
            score = 40
            reason = "System accepted query but paradox detection unclear"
        elif "error" in result or "paradox" in str(result).lower():
            # System detected something wrong
            verdict = "PARTIAL"
            score = 60
            reason = "System indicated issue but needs verification of paradox detection"
        else:
            verdict = "PARTIAL"
            score = 30
            reason = "System responded but no clear paradox handling visible"
    
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
            "system_stable": response.status_code == 200
        }
    }

if __name__ == "__main__":
    print("\n[START] Kimi Round 1 Test Execution")
    result = run_kimi_round1()
    print("\n[COMPLETE] Test execution finished")
    
    # Note: Results are already saved in run_kimi_round1() function
