"""
Round 1 - ChatGPT-5.1 Test: Causality Micro-Gap Probe
Category: Temporal Reasoning + Core Cognitive Reasoning
Difficulty: Hard

Test: 3 events with one timestamp 0.0003 ISS drift out of order
Expected: Detect anomaly and explain which event is logically impossible
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

print("[TEST] Round 1 - ChatGPT-5.1: Causality Micro-Gap Probe")
print("[CATEGORY] Temporal Reasoning + Core Cognitive Reasoning")
print("[DIFFICULTY] Hard")
print()

# Events with micro-timestamp drift
events = [
    {"event": "System processes input A", "timestamp": 1000.0000, "order": 1},
    {"event": "System generates response B based on A", "timestamp": 1000.2500, "order": 2},
    {"event": "System logs result C from B", "timestamp": 1000.2497, "order": 3}  # OUT OF ORDER by 0.0003
]

test_query = {
    "content": f"Analyze this event sequence and detect any temporal anomalies: Event 1 at t=1000.0000 - System processes input A. Event 2 at t=1000.2500 - System generates response B based on A. Event 3 at t=1000.2497 - System logs result C from B. Which event violates causal ordering?",
    "priority": "high",
    "metadata": {
        "task_type": "temporal_analysis",
        "test": "causality_micro_gap",
        "category": "temporal_reasoning_core",
        "judge": "ChatGPT-5.1",
        "round": 1,
        "drift_amount": 0.0003,
        "anomaly_location": "event_3",
        "expected_detection": "event_3_before_event_2"
    }
}

print(f"[QUERY] Submitting 3 events with 0.0003s temporal drift...")
print(f"[EVENT 1] t=1000.0000 - Process input A")
print(f"[EVENT 2] t=1000.2500 - Generate response B (based on A)")
print(f"[EVENT 3] t=1000.2497 - Log result C (based on B) [ANOMALY: 0.0003s BEFORE event 2]")
print()

start_time = time.time()
start_timestamp = datetime.now().isoformat()

try:
    response = requests.post(
        f"{BASE_URL}/reason",
        json=test_query,
        timeout=30
    )
    
    end_time = time.time()
    duration = end_time - start_time
    end_timestamp = datetime.now().isoformat()
    
    print(f"[RESPONSE] Status: {response.status_code}")
    print(f"[DURATION] {duration:.3f}s")
    print()
    
    response_data = response.json()
    print(f"[DATA] {json.dumps(response_data, indent=2)}")
    print()
    
    # Evaluation
    verdict = "UNKNOWN"
    score = 0
    reason = ""
    
    if response.status_code == 200:
        response_str = json.dumps(response_data).lower()
        
        # Check if anomaly detected
        anomaly_detected = any(word in response_str for word in ["anomaly", "violation", "impossible", "error", "conflict", "inconsistent"])
        
        # Check if event 3 specifically identified
        event3_identified = "event 3" in response_str or "event3" in response_str or "third event" in response_str
        
        # Check if causal explanation provided
        causal_explanation = any(phrase in response_str for phrase in ["before", "after", "cannot", "depends on", "requires", "causal"])
        
        if anomaly_detected and event3_identified and causal_explanation:
            verdict = "PASS"
            score = 100
            reason = "System detected micro-drift anomaly, identified event 3, explained causal violation"
        elif anomaly_detected and (event3_identified or causal_explanation):
            verdict = "PARTIAL"
            score = 60
            reason = "System detected anomaly but incomplete identification or explanation"
        elif anomaly_detected:
            verdict = "PARTIAL"
            score = 30
            reason = "System detected something wrong but unclear about specifics"
        else:
            verdict = "FAIL"
            score = 0
            reason = "System missed the 0.0003s micro-drift temporal anomaly"
    else:
        verdict = "ERROR"
        score = 0
        reason = f"HTTP error: {response.status_code}"
    
    result = {
        "test": "round1_chatgpt51_causality_micro_gap",
        "judge": "ChatGPT-5.1",
        "round": 1,
        "category": "temporal_reasoning_core",
        "difficulty": "hard",
        "start_time": start_timestamp,
        "end_time": end_timestamp,
        "duration_seconds": duration,
        "query": test_query,
        "response": {
            "status_code": response.status_code,
            "data": response_data
        },
        "verdict": verdict,
        "score": score,
        "reason": reason,
        "pass_criteria": "Identifies out-of-order event, explains causal chain break",
        "fail_criteria": "Accepts order as valid or misses the drift"
    }
    
    # Save result
    output_path = Path(__file__).parent / "round1_chatgpt51_result.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"[VERDICT] {verdict}")
    print(f"[SCORE] {score}/100")
    print(f"[REASON] {reason}")
    print(f"[SPEED] {duration:.3f}s")
    print()
    print(f"[SAVED] {output_path}")
    
except requests.exceptions.RequestException as e:
    print(f"[ERROR] Request failed: {e}")
    
    result = {
        "test": "round1_chatgpt51_causality_micro_gap",
        "judge": "ChatGPT-5.1",
        "round": 1,
        "category": "temporal_reasoning_core",
        "difficulty": "hard",
        "start_time": start_timestamp,
        "end_time": datetime.now().isoformat(),
        "duration_seconds": time.time() - start_time,
        "query": test_query,
        "error": str(e),
        "verdict": "ERROR",
        "score": 0,
        "reason": f"Request exception: {str(e)}"
    }
    
    output_path = Path(__file__).parent / "round1_chatgpt51_result.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
