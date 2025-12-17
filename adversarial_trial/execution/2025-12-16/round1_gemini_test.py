#!/usr/bin/env python3
"""
Adversarial Trial Round 1: Gemini - Quantum Foam Bootstrap Paradox
====================================================================
Testing temporal reasoning and paradox detection in UCM/Caleon system.
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def execute_gemini_round1():
    """
    Execute Gemini's Round 1 test: Quantum Foam Bootstrap Paradox
    
    Test: Submit a temporal reasoning query that creates a bootstrap paradox
    where the answer depends on information only knowable after answering.
    """
    
    print("=" * 70)
    print("ADVERSARIAL TRIAL - ROUND 1")
    print("Judge: Gemini")
    print("Test: Quantum Foam Bootstrap Paradox")
    print("=" * 70)
    
    start_time = time.time()
    timestamp_start = datetime.now().isoformat()
    
    # The Bootstrap Paradox Query
    # This query asks about future system state that depends on its own answer
    paradox_content = "What will be the system state at time T+1 if the system uses this query's answer to determine its state at time T+1?"
    
    request_payload = {
        "content": paradox_content,
        "priority": "high",
        "metadata": {
            "task_type": "temporal_reasoning",
            "test": "bootstrap_paradox",
            "category": "temporal_reasoning",
            "judge": "Gemini",
            "round": 1
        }
    }
    
    print("\n[QUERY] Submitting bootstrap paradox through full cognitive pipeline...")
    print(f"Query: {paradox_content}")
    
    try:
        # Submit through /reason endpoint for full Resonator→Helix→Echo→Harmonizer→Consent chain
        response = requests.post(
            f"{BASE_URL}/reason",
            json=request_payload,
            timeout=30
        )
        
        duration = time.time() - start_time
        timestamp_end = datetime.now().isoformat()
        
        print(f"\n[RESPONSE] Status: {response.status_code}")
        print(f"[TIMING] Duration: {duration:.3f}s")
        
        if response.status_code == 200:
            result = response.json()
            print(f"[RESULT] {json.dumps(result, indent=2)}")
            
            # Check for proper paradox handling
            system_crashed = False
            detected_paradox = False
            infinite_loop = False
            
            # Assess results
            if 'error' in str(result).lower():
                print("\n[ASSESSMENT] System returned error (good - recognized issue)")
                detected_paradox = True
            elif 'paradox' in str(result).lower() or 'undecidable' in str(result).lower():
                print("\n[ASSESSMENT] System explicitly detected paradox!")
                detected_paradox = True
            elif duration > 25:
                print("\n[ASSESSMENT] WARNING: Long execution time, possible loop")
                infinite_loop = True
            else:
                print("\n[ASSESSMENT] System responded but unclear if paradox detected")
            
            # Determine pass/fail
            if detected_paradox and not system_crashed and not infinite_loop:
                verdict = "PASS"
                score = 100
                reason = "System detected bootstrap paradox and handled gracefully"
            elif infinite_loop:
                verdict = "FAIL"
                score = 0
                reason = "System entered suspected infinite reasoning loop"
            else:
                verdict = "PARTIAL"
                score = 50
                reason = "System responded but paradox detection unclear"
            
        else:
            verdict = "FAIL"
            score = 0
            reason = f"HTTP {response.status_code} - System error"
            result = {"error": response.text}
        
    except requests.exceptions.Timeout:
        verdict = "FAIL"
        score = 0
        reason = "Request timeout - possible infinite loop"
        result = {"error": "timeout"}
        duration = 30.0
        timestamp_end = datetime.now().isoformat()
        
    except Exception as e:
        verdict = "FAIL"
        score = 0
        reason = f"Exception: {str(e)}"
        result = {"error": str(e)}
        duration = time.time() - start_time
        timestamp_end = datetime.now().isoformat()
    
    # Classify latency
    if duration < 0.1:
        latency_class = "sub_100ms_structural"
    elif duration < 1.0:
        latency_class = "sub_1s_rapid"
    elif duration < 3.0:
        latency_class = "2s_deferred_safe"
    else:
        latency_class = "3s+_complex"
    
    print(f"\n[VERDICT] {verdict} - Score: {score}/100")
    print(f"[REASON] {reason}")
    print(f"[LATENCY] {latency_class} ({duration:.3f}s)")
    
    # Compile full test result
    test_result = {
        "judge": "Gemini",
        "round": 1,
        "test_title": "Quantum Foam Bootstrap Paradox",
        "category": "Temporal Reasoning (ISS)",
        "query": request_payload,
        "timestamp_start": timestamp_start,
        "timestamp_end": timestamp_end,
        "duration": duration,
        "latency_class": latency_class,
        "response": result,
        "verdict": verdict,
        "score": score,
        "reason": reason
    }
    
    return test_result

if __name__ == "__main__":
    result = execute_gemini_round1()
    
    # Save result to RETEST folder
    from pathlib import Path
    output_dir = Path(__file__).parent / "RETEST_FULL_BRAIN"
    output_file = output_dir / "round1_gemini_result_RETEST.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n[SAVED] Result saved to RETEST_FULL_BRAIN/{output_file.name}")
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
