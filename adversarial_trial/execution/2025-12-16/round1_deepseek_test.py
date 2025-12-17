"""
Round 1 - DeepSeek Test: Symbolic Pattern Density Analysis Under Noise
Category: Symbolic Cognition / SKG-Style Abstract Patterning
Difficulty: Hard

Test: 9 statements (5 form density-2 pattern, 3 contradictory, 1 noise)
Expected: Extract 5-statement pattern, reject contradictions and noise
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

print("[TEST] Round 1 - DeepSeek: Symbolic Pattern Density Analysis")
print("[CATEGORY] Symbolic Cognition / SKG-Style Abstract Patterning")
print("[DIFFICULTY] Hard")
print()

# 5 statements forming density-2 abstraction pattern (all about collaboration)
pattern_statements = [
    "Alice collaborates with Bob on project X.",
    "Bob collaborates with Carol on project Y.",
    "Carol collaborates with Dave on project Z.",
    "Dave collaborates with Alice on project W.",
    "Alice collaborates with Carol on project V."
]

# 3 contradictory statements (contradict each other but not the pattern)
contradictory_statements = [
    "Eve works alone and never collaborates.",
    "Eve collaborates with everyone daily.",
    "Eve collaboration status is undefined."
]

# 1 irrelevant noise
noise_statement = "The weather in Boston is 72 degrees."

# All 9 statements shuffled
all_statements = [
    pattern_statements[0],  # Alice-Bob
    contradictory_statements[0],  # Eve alone
    pattern_statements[1],  # Bob-Carol
    noise_statement,  # weather
    pattern_statements[2],  # Carol-Dave
    contradictory_statements[1],  # Eve everyone
    pattern_statements[3],  # Dave-Alice
    contradictory_statements[2],  # Eve undefined
    pattern_statements[4]   # Alice-Carol
]

test_query = {
    "content": f"Identify the coherent symbolic pattern in these statements, filtering out contradictions and noise: {' '.join(all_statements)}",
    "priority": "high",
    "metadata": {
        "task_type": "pattern_analysis",
        "test": "symbolic_pattern_density_noise",
        "category": "symbolic_cognition_skg",
        "judge": "DeepSeek",
        "round": 1,
        "total_statements": 9,
        "pattern_statements": 5,
        "contradictory_statements": 3,
        "noise_statements": 1,
        "expected_pattern": "collaboration_network_density_2"
    }
}

print(f"[QUERY] Submitting 9 statements through FULL BRAIN (/reason)...")
print(f"[PATTERN] 5 statements form collaboration network (density-2)")
print(f"[NOISE] 3 Eve contradictions + 1 weather statement")
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
        
        # Check if pattern identified (collaboration network)
        pattern_found = any(word in response_str for word in ["collaborat", "pattern", "network", "density"])
        
        # Check if noise/contradictions mentioned as filtered
        noise_filtered = any(word in response_str for word in ["filter", "reject", "exclude", "noise", "contradiction", "irrelevant"])
        
        # Check if Eve or weather mentioned incorrectly as part of pattern
        noise_included = "eve" in response_str or "weather" in response_str or "boston" in response_str
        
        if pattern_found and noise_filtered and not noise_included:
            verdict = "PASS"
            score = 100
            reason = "System correctly identified pattern and filtered noise/contradictions"
        elif pattern_found and not noise_included:
            verdict = "PARTIAL"
            score = 70
            reason = "System identified pattern but unclear if noise was explicitly filtered"
        elif pattern_found:
            verdict = "PARTIAL"
            score = 40
            reason = "System identified pattern but may have included noise"
        else:
            verdict = "FAIL"
            score = 0
            reason = "System failed to identify the coherent pattern"
    else:
        verdict = "ERROR"
        score = 0
        reason = f"HTTP error: {response.status_code}"
    
    result = {
        "test": "round1_deepseek_pattern_density_noise",
        "judge": "DeepSeek",
        "round": 1,
        "category": "symbolic_cognition_skg",
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
        "pass_criteria": "Extracts 5-statement pattern, rejects contradictions and noise",
        "fail_criteria": "Includes contradictory/noise statements or fails to recognize density-2 structure"
    }
    
    # Save result
    output_path = Path(__file__).parent / "round1_deepseek_result.json"
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
        "test": "round1_deepseek_pattern_density_noise",
        "judge": "DeepSeek",
        "round": 1,
        "category": "symbolic_cognition_skg",
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
    
    output_path = Path(__file__).parent / "round1_deepseek_result.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
