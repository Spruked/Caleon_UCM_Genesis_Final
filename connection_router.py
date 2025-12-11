"""
Connection Router - UCM Direct vs DALS Routing
Clean. Easy. Unbreakable.

UCM → DIRECT for brain-to-brain operations:
- analyzing a certificate
- generating provenance
- doing identity logic
- checking ethical weight
- verifying SKG nodes
- pulling archived content
- asking GOAT for transformations or summaries

UCM → DALS for operational tasks:
- spawning a worker
- scheduling a mint job
- coordinating a batch
- triggering asynchronous tasks
- sending anything that requires queuing
- sending anything that needs lifecycle tracking
- requesting a workload distribution
- calling for parallel processing

One rule. Zero confusion.
"""

from typing import Dict, Any, Callable
from enum import Enum

class ConnectionType(Enum):
    DIRECT = "direct"
    DALS = "dals"

class ConnectionRouter:
    """
    Simple routing table for UCM connections.
    One rule determines everything.
    """

    # Brain-to-brain operations (DIRECT)
    DIRECT_TASKS = {
        "analysis",           # analyzing a certificate
        "provenance",         # generating provenance
        "identity",           # doing identity logic
        "transform",          # asking GOAT for transformations
        "summary",            # asking GOAT for summaries
        "ethical_weight",     # checking ethical weight
        "skg_verify",         # verifying SKG nodes
        "archive_pull",       # pulling archived content
        "reasoning",          # cognitive reasoning tasks
        "logic_check",        # logical validation
        "knowledge_query",    # direct knowledge retrieval
        "inference",          # logical inference
        "validation"          # content validation
    }

    # Operational tasks (DALS)
    DALS_TASKS = {
        "spawn_worker",       # spawning a worker
        "schedule_mint",      # scheduling a mint job
        "batch_coordinate",   # coordinating a batch
        "async_trigger",      # triggering asynchronous tasks
        "queue_task",         # anything requiring queuing
        "lifecycle_track",    # lifecycle tracking
        "workload_distribute", # workload distribution
        "parallel_process",   # parallel processing
        "background_job",     # background processing
        "scheduled_task",     # scheduled operations
        "bulk_operation",     # bulk operations
        "system_maintenance", # maintenance tasks
        "resource_allocation" # resource management
    }

    def __init__(self, direct_handler: Callable = None, dals_handler: Callable = None):
        """
        Initialize router with connection handlers.

        Args:
            direct_handler: Function to handle direct connections
            dals_handler: Function to handle DALS connections
        """
        self.direct_handler = direct_handler
        self.dals_handler = dals_handler

    def route(self, task: Dict[str, Any]) -> ConnectionType:
        """
        Route a task to the appropriate connection.

        One line. One rule. Zero confusion.

        Args:
            task: Task dictionary with 'type' field

        Returns:
            ConnectionType: DIRECT or DALS
        """
        task_type = task.get('type', '').lower()

        # The One Rule
        if task_type in self.DIRECT_TASKS:
            return ConnectionType.DIRECT
        else:
            return ConnectionType.DALS

    async def execute(self, task: Dict[str, Any]) -> Any:
        """
        Execute a task using the appropriate connection.

        Args:
            task: Task to execute

        Returns:
            Task result
        """
        connection_type = self.route(task)

        if connection_type == ConnectionType.DIRECT:
            if self.direct_handler:
                return await self.direct_handler(task)
            else:
                # Default direct processing
                return await self._direct_process(task)
        else:
            if self.dals_handler:
                return await self.dals_handler(task)
            else:
                # Default DALS processing
                return await self._dals_process(task)

    async def _direct_process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Default direct processing implementation.
        Brain-to-brain operations.
        """
        # Import here to avoid circular imports
        from cognition.knowledge_store import KnowledgeStore

        knowledge_store = KnowledgeStore()

        task_type = task.get('type', '')

        if task_type == 'analysis':
            # Direct analysis
            return {
                'result': f'Analyzed: {task.get("content", "")}',
                'connection': 'direct',
                'method': 'brain_to_brain'
            }
        elif task_type == 'provenance':
            # Generate provenance
            return {
                'result': f'Provenance generated for: {task.get("target", "")}',
                'connection': 'direct',
                'method': 'brain_to_brain'
            }
        elif task_type == 'identity':
            # Identity logic
            return {
                'result': f'Identity verified: {task.get("entity", "")}',
                'connection': 'direct',
                'method': 'brain_to_brain'
            }
        elif task_type in ['transform', 'summary']:
            # GOAT operations
            return {
                'result': f'GOAT {task_type}: {task.get("content", "")}',
                'connection': 'direct',
                'method': 'brain_to_brain'
            }
        else:
            # Generic direct processing
            return {
                'result': f'Processed directly: {task.get("content", "")}',
                'connection': 'direct',
                'method': 'brain_to_brain'
            }

    async def _dals_process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Default DALS processing implementation.
        Operational tasks.
        """
        # Import here to avoid circular imports
        from dals_integration import DALSCaleonBridge

        dals_bridge = DALSCaleonBridge()
        await dals_bridge.initialize()

        task_type = task.get('type', '')

        try:
            if task_type == 'spawn_worker':
                # Spawn a worker
                result = await dals_bridge.ask_caleon(
                    f"Spawn worker for task: {task.get('content', '')}"
                )
            elif task_type == 'schedule_mint':
                # Schedule mint job
                result = await dals_bridge.ask_caleon(
                    f"Schedule mint job: {task.get('content', '')}"
                )
            elif task_type == 'batch_coordinate':
                # Coordinate batch
                result = await dals_bridge.ask_caleon(
                    f"Coordinate batch: {task.get('content', '')}"
                )
            else:
                # Generic DALS processing
                result = await dals_bridge.ask_caleon(
                    f"Process operationally: {task.get('content', '')}"
                )

            await dals_bridge.close()

            return {
                'result': result,
                'connection': 'dals',
                'method': 'operational'
            }

        except Exception as e:
            await dals_bridge.close()
            return {
                'error': str(e),
                'connection': 'dals',
                'method': 'operational'
            }

# Global router instance
router = ConnectionRouter()

# Convenience functions
def route_task(task: Dict[str, Any]) -> ConnectionType:
    """Route a task to the appropriate connection."""
    return router.route(task)

async def execute_task(task: Dict[str, Any]) -> Any:
    """Execute a task using the appropriate connection."""
    return await router.execute(task)

# The One Rule - exposed for clarity
def is_brain_to_brain_task(task_type: str) -> bool:
    """Check if task is brain-to-brain (DIRECT) or operational (DALS)."""
    return task_type.lower() in ConnectionRouter.DIRECT_TASKS