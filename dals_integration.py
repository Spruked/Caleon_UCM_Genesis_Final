"""
DALS Integration with UCM
Example of how DALS connects to the central Caleon service
"""

import asyncio
import os
from shared.ucm_client.ucm import CaleonClient

class DALSCaleonBridge:
    def __init__(self):
        self.caleon = CaleonClient(
            base_url=os.getenv('UCM_URL', 'http://localhost:8000')
        )
        self.session_id = None

    async def initialize(self):
        """Initialize DALS session with Caleon"""
        session = await self.caleon.create_session()
        self.session_id = session['session_id']
        print(f'DALS Caleon session initialized: {self.session_id}')

    async def ask_caleon(self, message: str, user: str = 'dals_user'):
        """Ask Caleon a question"""
        try:
            response = await self.caleon.ask(message, self.session_id, user)
            return response
        except Exception as e:
            print(f'DALS Caleon error: {e}')
            raise e

    async def stream_caleon(self, message: str, on_token, user: str = 'dals_user'):
        """Stream Caleon's response"""
        try:
            await self.caleon.stream(message, on_token, self.session_id, user)
        except Exception as e:
            print(f'DALS Caleon stream error: {e}')
            raise e

    async def learn_fact(self, fact: str):
        """Teach Caleon a new fact"""
        return await self.caleon.learn(fact)

    async def set_user_preference(self, user: str, key: str, value: str):
        """Set user preference"""
        return await self.caleon.set_preference(user, key, value)

    async def close(self):
        """Close the connection"""
        await self.caleon.close()

# Singleton instance
dals_caleon = DALSCaleonBridge()

# Synchronous wrapper for easier use in synchronous contexts
class DALSCaleonSync:
    def __init__(self):
        self.async_bridge = dals_caleon

    def initialize(self):
        return asyncio.run(self.async_bridge.initialize())

    def ask_caleon(self, message: str, user: str = 'dals_user'):
        return asyncio.run(self.async_bridge.ask_caleon(message, user))

    def learn_fact(self, fact: str):
        return asyncio.run(self.async_bridge.learn_fact(fact))

    def set_user_preference(self, user: str, key: str, value: str):
        return asyncio.run(self.async_bridge.set_user_preference(user, key, value))

    def close(self):
        return asyncio.run(self.async_bridge.close())

# Export both async and sync versions
__all__ = ['dals_caleon', 'DALSCaleonSync']

# Example usage in DALS:
"""
# Initialize on startup
dals_bridge = DALSCaleonSync()
dals_bridge.initialize()

# Use in legal analysis
response = dals_bridge.ask_caleon("Analyze this contract for risks")

# Learn from legal precedents
dals_bridge.learn_fact("Contract clause X has been ruled invalid in jurisdiction Y")

# Set user preferences
dals_bridge.set_user_preference("lawyer@example.com", "analysis_depth", "detailed")
"""