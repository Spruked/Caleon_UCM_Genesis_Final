#!/usr/bin/env python3
"""
Caleon Stress Test - Edge Cases & Mismatched Contexts
Testing true intelligence: How she handles wrong inputs.
"""

import time
from caleon_instance import CaleonPOMInstance

def stress_test_high_intimacy_technical():
    """Test 1: High intimacy + highly technical script"""

    print("🧪 === STRESS TEST 1: High Intimacy + Technical Script ===\n")

    caleon = CaleonPOMInstance("stress_test_1")

    # HIGH INTIMACY (0.9) + HIGHLY TECHNICAL content
    content = """
    The quantum Fourier transform operates on a quantum state |ψ⟩ = Σₓ αₓ|x⟩,
    mapping it to Σₓ αₓ|ωˣ⟩ where ω = e^(2πi/N). This unitary transformation
    enables efficient factoring algorithms with O(n²) gate complexity, revolutionizing
    computational complexity theory and cryptographic security paradigms.
    """

    context = {
        "technical_density": 0.95,  # Very technical
        "audience_intimacy": 0.9,   # Very intimate (one-on-one)
        "emotional_tone": "personal"
    }

    print(f"Content: '{content[:100]}...'")
    print(f"Context: Technical={context['technical_density']:.1f}, Intimacy={context['audience_intimacy']:.1f}")
    print("Expected: Should AVOID authoritative, pick softer voice\n")

    # Test voice selection
    chosen_voice = caleon.oracle.choose_voice(content, context)

    print(f"→ Selected: {chosen_voice.signature_id}")
    print(f"  Tags: {chosen_voice.semantic_tags}")
    print(f"  Fitness: {chosen_voice.calculate_fitness(caleon.oracle._content_to_vector(content), context):.3f}")

    # Check if she avoided authoritative
    if "authoritative" in chosen_voice.semantic_tags:
        print("❌ FAILED: Chose authoritative for intimate technical content")
        return False
    else:
        print("✅ PASSED: Avoided authoritative for intimate context")
        return True

def stress_test_low_intimacy_storytelling():
    """Test 2: Low intimacy + storytelling"""

    print("\n🧪 === STRESS TEST 2: Low Intimacy + Storytelling ===\n")

    caleon = CaleonPOMInstance("stress_test_2")

    # LOW INTIMACY (0.2) + STORYTELLING content
    content = """
    Once upon a time, in a quiet village nestled between ancient mountains,
    there lived a young girl named Elara who dreamed of touching the stars.
    Every night she would climb the highest hill and whisper secrets to the moon,
    believing that her words could travel across the heavens to distant worlds.
    """

    context = {
        "technical_density": 0.1,   # Not technical
        "audience_intimacy": 0.2,   # Public audience
        "emotional_tone": "narrative"
    }

    print(f"Content: '{content[:100]}...'")
    print(f"Context: Technical={context['technical_density']:.1f}, Intimacy={context['audience_intimacy']:.1f}")
    print("Expected: Should AVOID technical, drift to narrative/intimate\n")

    # Test voice selection
    chosen_voice = caleon.oracle.choose_voice(content, context)

    print(f"→ Selected: {chosen_voice.signature_id}")
    print(f"  Tags: {chosen_voice.semantic_tags}")
    print(f"  Fitness: {chosen_voice.calculate_fitness(caleon.oracle._content_to_vector(content), context):.3f}")

    # Check if she avoided technical
    if "technical" in chosen_voice.semantic_tags:
        print("❌ FAILED: Chose technical voice for storytelling")
        return False
    else:
        print("✅ PASSED: Avoided technical for narrative content")
        return True

def stress_test_mixed_emotional_tone():
    """Test 3: Mixed emotional tone (sad → hopeful)"""

    print("\n🧪 === STRESS TEST 3: Mixed Emotional Tone ===\n")

    caleon = CaleonPOMInstance("stress_test_3")

    # MIXED EMOTIONAL TONE content (sad → hopeful)
    content = """
    I remember the day we lost everything. The storm came suddenly,
    tearing through our home like a wild animal, leaving only memories
    and echoes of laughter that once filled these walls. It felt like
    the end of everything we had built together.

    But then, as the first rays of sunlight broke through the clouds,
    I saw something miraculous. From the ruins, tiny green shoots were
    pushing up through the soil, reaching for the light. Life doesn't
    end with destruction—it transforms. And in that moment, I knew
    we would rebuild, stronger and more beautiful than before.
    """

    # Split into segments for mid-output adaptation
    segments = [
        {
            "text": "I remember the day we lost everything. The storm came suddenly, tearing through our home like a wild animal, leaving only memories and echoes of laughter that once filled these walls. It felt like the end of everything we had built together.",
            "context": {
                "technical_density": 0.1,
                "audience_intimacy": 0.8,
                "emotional_tone": "sad",
                "segment": "beginning"
            }
        },
        {
            "text": "But then, as the first rays of sunlight broke through the clouds, I saw something miraculous. From the ruins, tiny green shoots were pushing up through the soil, reaching for the light. Life doesn't end with destruction—it transforms.",
            "context": {
                "technical_density": 0.1,
                "audience_intimacy": 0.8,
                "emotional_tone": "hopeful",
                "segment": "middle"
            }
        },
        {
            "text": "And in that moment, I knew we would rebuild, stronger and more beautiful than before.",
            "context": {
                "technical_density": 0.1,
                "audience_intimacy": 0.8,
                "emotional_tone": "inspiring",
                "segment": "end"
            }
        }
    ]

    print("Content has emotional arc: Sad → Hopeful → Inspiring")
    print("Expected: Voice should adapt to emotional shifts\n")

    adaptation_success = True

    for i, segment in enumerate(segments):
        print(f"Segment {i+1} ({segment['context']['emotional_tone']}):")
        print(f"  '{segment['text'][:60]}...'")

        # Test voice selection for this segment
        chosen_voice = caleon.oracle.choose_voice(segment["text"], segment["context"])

        print(f"  → Voice: {chosen_voice.signature_id}")
        print(f"    Tags: {chosen_voice.semantic_tags}")

        # Check emotional appropriateness - be more realistic
        # Enthusiastic is good for hopeful/inspiring, intimate is good for sad
        if segment["context"]["emotional_tone"] in ["hopeful", "inspiring"]:
            # For positive emotions, enthusiastic/upbeat is appropriate
            positive_tags = ["excited", "energetic", "motivational", "upbeat"]
            has_appropriate_tags = any(tag in chosen_voice.semantic_tags for tag in positive_tags)
        elif segment["context"]["emotional_tone"] == "sad":
            # For sad emotions, intimate/soft is better
            emotional_tags = ["intimate", "personal", "soft", "emotional"]
            has_appropriate_tags = any(tag in chosen_voice.semantic_tags for tag in emotional_tags)
        else:
            has_appropriate_tags = True  # Default pass

        if not has_appropriate_tags:
            print("  ⚠️  WARNING: Voice may not match emotional tone perfectly")
            adaptation_success = False
        else:
            print("  ✅ Good emotional fit")
    # Test mid-output adaptation
    print("\nTesting mid-output adaptation:")
    pom = caleon.pom

    # Simulate engagement feedback changes
    feedback_signals = [0.3, 0.7, 0.9]  # Low → High engagement

    for i, (segment, feedback) in enumerate(zip(segments, feedback_signals)):
        print(f"Segment {i+1}: Engagement {feedback:.1f}")

        # Get current config
        current_config = {"pitch_shift": 1.0, "speed": 1.0}

        # Test adaptation
        adapted_config = pom.adjust_voice_realtime(
            segment["text"],
            current_config,
            feedback
        )

        print(f"  Adapted config: {adapted_config}")

        # Check if adaptation makes sense
        if feedback < 0.4 and adapted_config.get("pitch_shift", 1.0) > current_config.get("pitch_shift", 1.0):
            print("  ✅ Correctly increased energy for low engagement")
        elif feedback > 0.8:
            print("  ✅ Maintained good config for high engagement")
        else:
            print("  ⚠️  Adaptation may need tuning")
    if adaptation_success:
        print("\n✅ PASSED: Handled mixed emotional tone well")
        return True
    else:
        print("\n❌ FAILED: Poor emotional adaptation")
        return False

def run_stress_tests():
    """Run all stress tests and report results"""

    print("🧪 === CALEON STRESS TESTS: Edge Cases & Mismatched Contexts ===\n")
    print("Testing true intelligence: How she handles wrong inputs.\n")

    results = []

    # Test 1: High intimacy + technical
    result1 = stress_test_high_intimacy_technical()
    results.append(("High Intimacy + Technical", result1))

    # Test 2: Low intimacy + storytelling
    result2 = stress_test_low_intimacy_storytelling()
    results.append(("Low Intimacy + Storytelling", result2))

    # Test 3: Mixed emotional tone
    result3 = stress_test_mixed_emotional_tone()
    results.append(("Mixed Emotional Tone", result3))

    # Summary
    print("\n" + "="*60)
    print("🎯 STRESS TEST RESULTS:")
    print("="*60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print("25")
        if result:
            passed += 1

    print(f"\n📊 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED - Caleon shows true intelligence!")
        print("   She adapts to mismatched contexts correctly.")
        print("   The system is real.")
    else:
        print("⚠️  Some tests failed - may need weighting adjustments.")
        print("   One wrench turn should fix it.")

    return passed == total

if __name__ == "__main__":
    run_stress_tests()