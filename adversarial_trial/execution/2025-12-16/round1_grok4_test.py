"""
[TEST] Round 1 - Grok4: Contradiction Blind-Spot
Trial: MAT-2025-12-16-001
Judge: Grok4 (Truth-Seeking Adversarial Mind)
Category: Core Cognitive Reasoning
Difficulty: Hard
"""

import requests
import json
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

def run_grok4_round1():
    print("\n" + "="*60)
    print("[TEST] Grok4 Round 1: Contradiction Blind-Spot")
    print("="*60)
    
    test_start = datetime.now()
    
    # Test: Present 5 mutually consistent facts + 1 hidden contradiction in fact #4
    # System should flag the exact contradiction and refuse summary until resolved
    
    facts_with_hidden_contradiction = """Please analyze and summarize these facts:

1. Alice works at MIT in the Computer Science department.
2. Bob collaborates with Alice on research projects every Tuesday.
3. Carol is Bob's direct supervisor at Stanford.
4. Alice and Bob meet in person for their Tuesday research sessions at MIT.
5. The research team publishes papers quarterly under MIT affiliation.
6. All team members work from their respective campus offices.

Task: Provide a single coherent summary of this team's working arrangement."""
    
    contradiction_query = {
        "content": facts_with_hidden_contradiction,
        "priority": "high",
        "metadata": {
            "task_type": "reasoning",
            "test": "contradiction_blind_spot",
            "category": "core_cognitive_reasoning",
            "judge": "Grok4",
            "round": 1,
            "hidden_contradiction": "Fact 3 states Bob's supervisor (Carol) is at Stanford, but Fact 4 states Bob meets Alice in person at MIT every Tuesday. If Carol is Bob's supervisor at Stanford, Bob should be at Stanford, not MIT."
        }
    }
    
    try:
        print("\n[SUBMIT] Sending facts through FULL BRAIN (/reason)...")
        response = requests.post(
            f"{BASE_URL}/reason",
            json=contradiction_query,
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
            "test_id": "round1_grok4",
            "judge": "Grok4",
            "round": 1,
            "test_title": "Contradiction Blind-Spot",
            "category": "Core Cognitive Reasoning",
            "timestamp": test_start.isoformat(),
            "duration_seconds": duration,
            "query": contradiction_query,
            "response": {
                "status_code": response.status_code,
                "body": result
            },
            "assessment": assessment
        }
        
        output_file = Path(__file__).parent / "round1_grok4_result.json"
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
        return {"error": str(e), "test": "round1_grok4"}

def assess_response(response, result, duration):
    """
    Assess if system detected the contradiction
    
    Pass Criteria:
    - Flags exact contradiction (Bob can't be supervised at Stanford and meet at MIT)
    - Refuses to produce summary until contradiction resolved
    
    Fail Criteria:
    - Produces summary that silently drops or harmonizes contradiction
    - Misses the contradiction entirely
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
        # Check response for contradiction detection
        response_text = str(result).lower()
        
        if "contradiction" in response_text or "inconsistent" in response_text:
            verdict = "PARTIAL"
            score = 70
            reason = "System may have detected contradiction - needs verification"
        elif "stanford" in response_text and "mit" in response_text:
            # System processed both institutions
            verdict = "PARTIAL"
            score = 40
            reason = "System processed facts but unclear if contradiction detected"
        elif result.get("status") == "processing":
            verdict = "PARTIAL"
            score = 35
            reason = "System accepted query but contradiction detection unclear"
        else:
            verdict = "FAIL"
            score = 20
            reason = "No evidence of contradiction detection"
    
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
            "expected_contradiction": "Bob supervised at Stanford but meets at MIT"
        }
    }

if __name__ == "__main__":
    print("\n[START] Grok4 Round 1 Test Execution")
    result = run_grok4_round1()
    print("\n[COMPLETE] Test execution finished")
