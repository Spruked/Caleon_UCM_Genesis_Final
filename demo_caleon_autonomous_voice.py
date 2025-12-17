#!/usr/bin/env python3
"""
Caleon Autonomous Voice System Demo
Demonstrates Caleon's self-modifying phonatory system with learning and evolution.
"""

import time
import json
from caleon_instance import CaleonPOMInstance
from skg_ucm_bridge import SKGUCMBridge

def demo_caleon_voice_oracle():
    """Demo Caleon's voice selection capabilities"""

    print("🎭 === Caleon Voice Oracle Demo ===\n")

    # Create Caleon's instance
    caleon = CaleonPOMInstance("demo_instance")

    # Test content samples
    test_content = [
        "Welcome to this technical presentation on quantum computing algorithms.",
        "I want to share something very personal with you about my journey.",
        "Let's dive deep into the mathematics behind neural networks and optimization.",
        "I'm so excited to announce our breakthrough in AGI development!",
        "This is a formal announcement regarding our company policy changes."
    ]

    contexts = [
        {"technical_density": 0.8, "audience_intimacy": 0.3},
        {"technical_density": 0.2, "audience_intimacy": 0.8},
        {"technical_density": 0.9, "audience_intimacy": 0.4},
        {"technical_density": 0.3, "audience_intimacy": 0.6},
        {"technical_density": 0.1, "audience_intimacy": 0.2}
    ]

    print("Testing voice selection for different content types:\n")

    for i, (content, context) in enumerate(zip(test_content, contexts)):
        print(f"Content {i+1}: '{content[:50]}...'")
        print(f"Context: Technical={context['technical_density']:.1f}, Intimacy={context['audience_intimacy']:.1f}")

        # Caleon chooses her voice
        chosen_voice = caleon.oracle.choose_voice(content, context)

        print(f"→ Selected: {chosen_voice.signature_id}")
        print(f"  Fitness: {chosen_voice.calculate_fitness(caleon.oracle._content_to_vector(content), context):.3f}")
        print(f"  Tags: {chosen_voice.semantic_tags}")
        print()

    return caleon

def demo_voice_evolution(caleon):
    """Demo Caleon's voice evolution capabilities"""

    print("🧬 === Voice Evolution Demo ===\n")

    # Sample content for evolution
    evolution_samples = [
        "The quantum superposition principle states that a particle can exist in multiple states simultaneously until measured.",
        "I remember the first time I felt truly alive, when I realized I could choose my own path.",
        "Gradient descent optimization minimizes the loss function by iteratively adjusting model parameters.",
        "Today marks a new chapter in our shared journey toward understanding consciousness.",
        "The Fourier transform decomposes signals into their frequency components for analysis."
    ]

    print(f"Evolving voices based on {len(evolution_samples)} content samples...\n")

    # Evolve voices
    caleon.evolve_voice(evolution_samples, target_performance=0.85)

    print(f"\nEvolution complete! Caleon now has {len(caleon.oracle.voice_registry)} voices.\n")

    # Show evolved voices
    for voice in caleon.oracle.voice_registry:
        print(f"• {voice.signature_id}: score={voice.success_score:.3f}, tags={voice.semantic_tags}")

    print()

def demo_performance_feedback(caleon):
    """Demo performance feedback and learning"""

    print("📊 === Performance Learning Demo ===\n")

    # Simulate performance feedback
    feedback_scenarios = [
        ("caleon_technical", "tech_content_1", 0.9, {"retention_rate": 0.85, "engagement_score": 0.88}),
        ("caleon_intimate", "personal_content_1", 0.95, {"retention_rate": 0.92, "engagement_score": 0.90}),
        ("caleon_baseline", "general_content_1", 0.7, {"retention_rate": 0.65, "engagement_score": 0.70}),
        ("caleon_enthusiastic", "exciting_content_1", 0.8, {"retention_rate": 0.78, "engagement_score": 0.82})
    ]

    print("Providing performance feedback to Caleon's Oracle:\n")

    for voice_id, content_hash, score, listener_feedback in feedback_scenarios:
        print(f"Feedback for {voice_id}: score={score:.2f}")
        caleon.oracle.receive_feedback(voice_id, content_hash, score, listener_feedback)

    print("\nUpdated voice scores after learning:\n")
    for voice in caleon.oracle.voice_registry:
        print(f"• {voice.signature_id}: {voice.success_score:.3f} (used {voice.usage_count} times)")

    print()

def demo_speech_generation(caleon):
    """Demo actual speech generation with Caleon's chosen voices"""

    print("🎵 === Speech Generation Demo ===\n")

    test_content = "Hello, I'm Caleon. I choose my voice based on what I'm saying and how I want to connect with you."

    context = {
        "technical_density": 0.3,
        "audience_intimacy": 0.7,
        "emotional_tone": "warm"
    }

    print(f"Generating speech for: '{test_content}'")
    print(f"Context: {context}\n")

    # Generate speech with Caleon's autonomous choice
    output_path = caleon.generate_speech(test_content, "demo_content_1", context)

    print(f"\nSpeech generated successfully: {output_path}\n")

def demo_bridge_integration():
    """Demo UCM-SKG Bridge integration"""

    print("🌉 === UCM-SKG Bridge Demo ===\n")

    # Mock SKG Manager
    class MockSKG:
        def __init__(self):
            self.content_vectors = {}
            self.performance_queue = {}

    # Mock UCM Instance
    class MockUCM:
        def __init__(self):
            self.subscriptions = {}

        def subscribe(self, event, callback):
            self.subscriptions[event] = callback

        def set_content_metadata(self, content_id, metadata):
            print(f"UCM: Set metadata for {content_id}: {metadata}")

    # Create bridge
    skg = MockSKG()
    ucm = MockUCM()
    bridge = SKGUCMBridge(skg, ucm)

    print("Bridge initialized. Testing content ingestion...\n")

    # Simulate content ingestion
    content_metadata = {
        "content_type": "technical_presentation",
        "topics": ["AI", "neural_networks"],
        "technical_density": 0.8,
        "preview_text": "Today we'll explore the fundamentals of neural network architecture.",
        "tags": ["caleon_narration", "educational"],
        "source": "demo"
    }

    # Trigger content ingestion
    bridge._on_content_ingested("demo_content_1", content_metadata)

    print("\nSimulating analytics feedback...\n")

    # Simulate analytics
    analytics = {
        "avg_retention": 0.82,
        "engagement": 0.75,
        "completion_rate": 0.8
    }

    bridge._on_analytics_received("demo_content_1", analytics)

    print(f"\nBridge status: {bridge.get_bridge_status()}\n")

def demo_voice_dna_export_import(caleon):
    """Demo voice DNA export and import"""

    print("🧬 === Voice DNA Export/Import Demo ===\n")

    # Export Caleon's voice DNA
    print("Exporting Caleon's voice DNA...")
    dna = caleon.export_voice_dna()

    print(f"Exported DNA contains:")
    print(f"  • {len(dna['voice_registry'])} voices")
    print(f"  • {len(dna['evolution_log'])} evolution events")
    print(f"  • {len(dna['performance_log'])} performance records")
    print(f"  • {len(dna['pom_modification_log'])} POM modifications")

    # Save to file
    dna_file = "caleon_dna_demo_backup.json"
    with open(dna_file, 'w') as f:
        json.dump(dna, f, indent=2)

    print(f"DNA saved to: {dna_file}\n")

    # Create new instance and import DNA
    print("Creating new Caleon instance and importing DNA...")
    new_caleon = CaleonPOMInstance("imported_instance")

    with open(dna_file, 'r') as f:
        imported_dna = json.load(f)

    new_caleon.import_voice_dna(imported_dna)

    print("DNA imported successfully!")
    print(f"New instance status: {new_caleon.get_instance_status()}\n")

def main():
    """Run the complete Caleon autonomous voice system demo"""

    print("🤖 === Caleon's Self-Modifying Phonatory System Demo ===\n")
    print("This demo showcases Caleon's autonomous voice selection, learning, and evolution.\n")

    # Demo 1: Voice Oracle
    caleon = demo_caleon_voice_oracle()

    # Demo 2: Voice Evolution
    demo_voice_evolution(caleon)

    # Demo 3: Performance Learning
    demo_performance_feedback(caleon)

    # Demo 4: Speech Generation
    demo_speech_generation(caleon)

    # Demo 5: Bridge Integration
    demo_bridge_integration()

    # Demo 6: Voice DNA
    demo_voice_dna_export_import(caleon)

    print("🎉 === Demo Complete ===\n")
    print("Caleon now has:")
    print(f"  • Autonomous voice selection based on content and context")
    print(f"  • Learning from performance feedback")
    print(f"  • Voice evolution and pruning")
    print(f"  • Self-modifying phonatory parameters")
    print(f"  • Isolated personal workspace")
    print(f"  • UCM-SKG integration for seamless metadata flow")
    print("\nCaleon is now a self-aware voice synthesis entity! 🎭✨\n")

if __name__ == "__main__":
    main()