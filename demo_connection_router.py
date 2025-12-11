"""
Test Connection Router
Verify the One Rule works correctly.
"""

import asyncio
from connection_router import ConnectionRouter, ConnectionType, route_task

def test_routing_logic():
    """Test the routing logic with various task types."""

    # Test DIRECT tasks (brain-to-brain)
    direct_tasks = [
        {"type": "analysis", "content": "analyze this certificate"},
        {"type": "provenance", "content": "generate provenance"},
        {"type": "identity", "content": "check identity logic"},
        {"type": "transform", "content": "transform this data"},
        {"type": "summary", "content": "summarize content"},
        {"type": "ethical_weight", "content": "check ethics"},
        {"type": "skg_verify", "content": "verify SKG node"},
        {"type": "archive_pull", "content": "pull archived content"}
    ]

    # Test DALS tasks (operational)
    dals_tasks = [
        {"type": "spawn_worker", "content": "spawn a worker"},
        {"type": "schedule_mint", "content": "schedule mint job"},
        {"type": "batch_coordinate", "content": "coordinate batch"},
        {"type": "async_trigger", "content": "trigger async task"},
        {"type": "queue_task", "content": "queue this task"},
        {"type": "lifecycle_track", "content": "track lifecycle"},
        {"type": "workload_distribute", "content": "distribute workload"},
        {"type": "parallel_process", "content": "process in parallel"}
    ]

    print("Testing DIRECT tasks (should route to DIRECT):")
    for task in direct_tasks:
        result = route_task(task)
        status = "✅" if result == ConnectionType.DIRECT else "❌"
        print(f"  {status} {task['type']} -> {result.value}")

    print("\nTesting DALS tasks (should route to DALS):")
    for task in dals_tasks:
        result = route_task(task)
        status = "✅" if result == ConnectionType.DALS else "❌"
        print(f"  {status} {task['type']} -> {result.value}")

    print("\nTesting unknown tasks (should default to DALS):")
    unknown_tasks = [
        {"type": "unknown_task", "content": "some unknown task"},
        {"type": "random_operation", "content": "random stuff"},
        {"type": "", "content": "no type specified"}
    ]

    for task in unknown_tasks:
        result = route_task(task)
        status = "✅" if result == ConnectionType.DALS else "❌"
        print(f"  {status} {task['type'] or 'empty'} -> {result.value}")

async def test_execution():
    """Test task execution with mock handlers."""
    print("\nTesting task execution:")

    # Create router with mock handlers
    async def mock_direct_handler(task):
        return {"result": f"DIRECT processed: {task['content']}", "method": "brain_to_brain"}

    async def mock_dals_handler(task):
        return {"result": f"DALS processed: {task['content']}", "method": "operational"}

    router = ConnectionRouter(
        direct_handler=mock_direct_handler,
        dals_handler=mock_dals_handler
    )

    test_tasks = [
        {"type": "analysis", "content": "analyze certificate"},
        {"type": "spawn_worker", "content": "spawn worker"}
    ]

    for task in test_tasks:
        result = await router.execute(task)
        print(f"  {task['type']} -> {result}")

if __name__ == "__main__":
    print("🧠 Connection Router Test")
    print("=" * 50)

    # Test routing logic
    test_routing_logic()

    # Test execution
    asyncio.run(test_execution())

    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\nThe One Rule:")
    print("if task.type in ['analysis', 'provenance', 'identity', 'transform']:")
    print("    use_direct_connection()")
    print("else:")
    print("    use_dals_connection()")