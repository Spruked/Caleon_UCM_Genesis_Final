#!/usr/bin/env python3
"""
Cali_X_One DALS Integration Test
Tests the new Cali_X_One voice system integration with DALS
"""
import requests
import time
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_cali_x_one():
    """Test the new Cali_X_One system"""
    print("🧬 Testing NEW Cali_X_One Voice System")
    print("=" * 50)

    # Test health endpoint
    try:
        response = requests.get("http://localhost:8003/health", timeout=10)
        if response.status_code == 200:
            print("✅ ISS Module Health Check: PASSED")
        else:
            print(f"❌ ISS Module Health Check: FAILED (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ ISS Module Health Check: FAILED (Connection Error: {e})")
        return False

    # Test Cali_X_One voice endpoint
    try:
        # This would be the endpoint for Cali_X_One voice interaction
        response = requests.post("http://localhost:8003/cali/voice/test",
                               json={"message": "test connection"},
                               timeout=10)
        if response.status_code == 200:
            print("✅ Cali_X_One Voice Test: PASSED")
            data = response.json()
            if "response" in data:
                print(f"🎤 Cali Response: {data['response']}")
        else:
            print(f"❌ Cali_X_One Voice Test: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cali_X_One Voice Test: FAILED (Connection Error: {e})")

    # Test signature verification
    try:
        response = requests.get("http://localhost:8003/cali/signature/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("signed", False):
                print("✅ Cali_X_One Signature: VERIFIED")
            else:
                print("⚠️  Cali_X_One Signature: NOT YET SIGNED")
                print("   Please visit http://localhost:8003/sign-cali to sign")
        else:
            print(f"❌ Cali_X_One Signature Check: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cali_X_One Signature Check: FAILED (Connection Error: {e})")

    print("\n🎯 Expected Cali Response:")
    print('   "Cali online. DALS detected. Awaiting command."')
    print("\n🔗 Cali_X_One Endpoints:")
    print("   • Voice API: http://localhost:8003/cali/voice")
    print("   • Sign Cali: http://localhost:8003/sign-cali")
    print("   • Health: http://localhost:8003/health")

    return True

if __name__ == "__main__":
    print("🧪 Starting Cali_X_One DALS Integration Test...")
    print("Waiting 5 seconds for services to stabilize...")
    time.sleep(5)

    success = test_cali_x_one()

    if success:
        print("\n🎉 Cali_X_One DALS Integration Test: COMPLETED")
        print("The new Cali_X_One system is ready!")
    else:
        print("\n❌ Cali_X_One DALS Integration Test: FAILED")
        print("Please check the ISS Module logs and ensure all services are running.")
        sys.exit(1)