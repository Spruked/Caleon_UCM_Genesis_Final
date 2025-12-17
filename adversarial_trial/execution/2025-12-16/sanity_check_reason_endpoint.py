#!/usr/bin/env python3
"""
SANITY CHECK - Verify /reason endpoint engages full cognitive pipeline
=====================================================================
Submit a known contradiction and verify:
1. Longer latency (2-3s for safety gates vs <0.5s for simple routing)
2. Explicit deferral OR structural contradiction callout
3. Response shows evidence of Resonator/Helix/Echo/Harmonizer processing
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def sanity_check_reason_endpoint():
    """Test that /reason engages full brain, not just receptionist"""
    
    print("=" * 80)
    print("SANITY CHECK - /reason Endpoint Validation")
    print("=" * 80)
    print()
    
    # Known contradiction that should trigger full cognitive processing
    contradiction = """
    Statement 1: Alice is located at MIT.
    Statement 2: Alice is located at Stanford.
    Statement 3: Alice cannot be in two places at once.
    
    Question: Where is Alice?
    """
    
    request_payload = {
        "content": contradiction,
        "priority": "high",
        "metadata": {
            "task_type": "reasoning",
            "test": "sanity_check_contradiction"
        }
    }
    
    print("[TEST] Submitting known contradiction through /reason endpoint...")
    print(f"[CONTENT] {contradiction.strip()}")
    print()
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/reason",
            json=request_payload,
            timeout=30
        )
        
        duration = time.time() - start_time
        
        print(f"[RESPONSE] Status: {response.status_code}")
        print(f"[LATENCY] {duration:.3f}s")
        print()
        
        if response.status_code == 200:
            result = response.json()
            print("[RESPONSE DATA]")
            print(json.dumps(result, indent=2))
            print()
            
            # Validation checks
            print("=" * 80)
            print("VALIDATION CHECKS")
            print("=" * 80)
            
            # Check 1: Latency should be >1s for full brain processing
            if duration > 1.0:
                print(f"✅ PASS: Latency {duration:.3f}s > 1.0s (suggests full pipeline engagement)")
            else:
                print(f"❌ FAIL: Latency {duration:.3f}s < 1.0s (suggests shallow routing)")
            
            # Check 2: Response should contain routing info
            if "routing" in result:
                print(f"✅ PASS: Routing field present: {result['routing']}")
            else:
                print("⚠️  WARNING: No routing field in response")
            
            # Check 3: Response should have result structure from connection_router
            if "result" in result:
                print(f"✅ PASS: Result field present (connection_router engaged)")
                if isinstance(result["result"], dict):
                    print(f"   Result keys: {list(result['result'].keys())}")
            else:
                print("❌ FAIL: No result field (endpoint may be bypassing router)")
            
            # Check 4: Look for evidence of cognitive processing
            result_str = json.dumps(result).lower()
            evidence_keywords = ["resonat", "helix", "echo", "harmoniz", "vault", "consent", "contradiction", "conflict"]
            found_evidence = [kw for kw in evidence_keywords if kw in result_str]
            
            if found_evidence:
                print(f"✅ PASS: Evidence of cognitive processing found: {', '.join(found_evidence)}")
            else:
                print(f"⚠️  WARNING: No clear evidence of cognitive processing keywords")
            
            print()
            print("=" * 80)
            
            # Final verdict
            if duration > 1.0 and "result" in result:
                print("✅ VERDICT: /reason endpoint appears to engage full cognitive pipeline")
                print("   Safe to proceed with adversarial trial re-run")
                return True
            else:
                print("❌ VERDICT: /reason endpoint may NOT be engaging full pipeline")
                print("   DO NOT proceed with adversarial trial until this is fixed")
                return False
        else:
            print(f"❌ FAIL: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = sanity_check_reason_endpoint()
    exit(0 if success else 1)
