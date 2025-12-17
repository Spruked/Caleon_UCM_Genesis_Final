"""
SKG-UCM Bridge - Seamless Integration Between Unified Content Manager and Speaker Knowledge Graph
Bidirectional sync so content metadata flows directly into voice selection.
"""

from typing import Dict, Any
import threading
import time
import json

class SKGUCMBridge:
    """
    Bidirectional sync between Unified Content Manager and Speaker Knowledge Graph
    """

    def __init__(self, skg_manager, ucm_instance):
        self.skg = skg_manager
        self.ucm = ucm_instance
        self.sync_lock = threading.Lock()

        # Subscribe to UCM content events
        self.ucm.subscribe("content_ingested", self._on_content_ingested)
        self.ucm.subscribe("content_published", self._on_content_published)
        self.ucm.subscribe("listener_analytics", self._on_analytics_received)

    def _on_content_ingested(self, content_id: str, metadata: Dict):
        """Auto-enrich SKG when UCM receives new content"""

        print(f"🌉 UCM→SKG: New content '{content_id}' ingested")

        with self.sync_lock:
            # Extract semantic features
            semantic_tags = self._extract_semantic_tags(metadata)

            # Create content vector in SKG
            self.skg.content_vectors[content_id] = {
                "vector": self._vectorize_content(metadata),
                "tags": semantic_tags,
                "timestamp": time.time(),
                "source": metadata.get("source", "unknown")
            }

            # If content is tagged for Caleon, notify Oracle
            if "caleon_narration" in metadata.get("tags", []):
                self._prepare_caleon_voice(content_id, metadata)

    def _on_content_published(self, content_id: str, publication_data: Dict):
        """Track voice usage when content goes live"""

        voice_used = publication_data.get("voice_signature_id")
        if voice_used and "caleon" in voice_used:
            print(f"🌉 Tracking: Caleon used {voice_used} for {content_id}")

            # Log in performance queue for later feedback
            self.skg.performance_queue[content_id] = {
                "voice_id": voice_used,
                "timestamp": time.time(),
                "status": "pending_feedback"
            }

    def _on_analytics_received(self, content_id: str, analytics: Dict):
        """Feed listener analytics back to Caleon's Oracle"""

        if content_id not in self.skg.performance_queue:
            return

        print(f"🌉 UCM→SKG: Analytics received for {content_id}")

        # Extract engagement metrics
        listener_feedback = {
            "retention_rate": analytics.get("avg_retention", 0.7),
            "engagement_score": analytics.get("engagement", 0.6),
            "completion_rate": analytics.get("completion_rate", 0.5),
            "drop_off_points": analytics.get("drop_off_timestamps", [])
        }

        # Calculate performance score
        performance_score = (
            listener_feedback["retention_rate"] * 0.4 +
            listener_feedback["engagement_score"] * 0.3 +
            listener_feedback["completion_rate"] * 0.3
        )

        # Send to Oracle for learning
        voice_id = self.skg.performance_queue[content_id]["voice_id"]

        # Import here to avoid circular imports
        from caleon_voice_oracle import CaleonVoiceOracle
        oracle = CaleonVoiceOracle()
        oracle.receive_feedback(
            voice_id=voice_id,
            content_hash=content_id,
            performance_score=performance_score,
            listener_feedback=listener_feedback
        )

        # Mark as processed
        self.skg.performance_queue[content_id]["status"] = "processed"

    def _extract_semantic_tags(self, metadata: Dict) -> list:
        """Extract semantic tags from content metadata"""

        tags = []

        # Content type tags
        content_type = metadata.get("content_type", "")
        if "technical" in content_type.lower():
            tags.extend(["technical", "educational"])
        elif "narrative" in content_type.lower():
            tags.extend(["storytelling", "narrative"])
        elif "conversational" in content_type.lower():
            tags.extend(["conversational", "casual"])

        # Topic-based tags
        topics = metadata.get("topics", [])
        tags.extend(topics)

        # Emotional tone
        tone = metadata.get("emotional_tone", "")
        if tone:
            tags.append(tone)

        return list(set(tags))  # Remove duplicates

    def _vectorize_content(self, metadata: Dict) -> list:
        """Create semantic vector from content metadata"""

        # Simple vectorization based on metadata
        # In production: use proper embeddings
        vector = []

        # Content length factor
        length = len(metadata.get("content", ""))
        vector.append(min(length / 10000, 1.0))  # Normalize

        # Technical density
        tech_density = metadata.get("technical_density", 0.5)
        vector.append(tech_density)

        # Emotional intensity
        emotion_intensity = metadata.get("emotional_intensity", 0.5)
        vector.append(emotion_intensity)

        # Complexity score
        complexity = metadata.get("complexity_score", 0.5)
        vector.append(complexity)

        return vector

    def _prepare_caleon_voice(self, content_id: str, metadata: Dict):
        """Pre-select voice signature for upcoming narration"""

        from caleon_voice_oracle import CaleonVoiceOracle
        oracle = CaleonVoiceOracle()

        # Extract content snippets
        content_preview = metadata.get("preview_text", "")

        context = {
            "technical_density": metadata.get("technical_density", 0.0),
            "emotional_tone": metadata.get("primary_emotion", "neutral"),
            "audience_intimacy": metadata.get("target_audience", "general"),
            "content_id": content_id
        }

        # This will pre-load her choice into the registry
        chosen_voice = oracle.choose_voice(content_preview, context)

        # Store choice in UCM for reference
        self.ucm.set_content_metadata(content_id, {
            "preselected_voice_id": chosen_voice.signature_id,
            "voice_fitness": chosen_voice.calculate_fitness(
                oracle._content_to_vector(content_preview),
                context
            )
        })

    def simulate_analytics_feedback(self, content_id: str, retention: float, engagement: float, completion: float = 0.5):
        """
        Simulate analytics feedback for testing/development
        """

        analytics = {
            "avg_retention": retention,
            "engagement": engagement,
            "completion_rate": completion,
            "drop_off_timestamps": []
        }

        self._on_analytics_received(content_id, analytics)

    def get_bridge_status(self) -> Dict:
        """Get current bridge status and metrics"""

        return {
            "active_subscriptions": ["content_ingested", "content_published", "listener_analytics"],
            "pending_feedback": len([p for p in self.skg.performance_queue.values() if p["status"] == "pending_feedback"]),
            "processed_feedback": len([p for p in self.skg.performance_queue.values() if p["status"] == "processed"]),
            "content_vectors_stored": len(self.skg.content_vectors)
        }