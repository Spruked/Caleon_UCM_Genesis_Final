"""
Caleon Cognitive Monitoring Dashboard
Real-time monitoring and visualization of the cognitive process pipeline
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
import asyncio
import httpx
from telemetry import cognitive_monitor, CognitiveMonitor
# from config import settings  # Temporarily commented out

app = FastAPI(title="Caleon Cognitive Monitoring Dashboard", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="monitoring/static"), name="static")
templates = Jinja2Templates(directory="monitoring/templates")

# Dashboard data cache
dashboard_cache = {
    "last_update": 0,
    "metrics": {},
    "alerts": []
}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main cognitive monitoring dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/metrics/current")
async def get_current_metrics():
    """Get current cognitive metrics for real-time dashboard"""
    try:
        # Get metrics from Prometheus endpoint if available
        prometheus_url = os.getenv('PROMETHEUS_URL', 'http://localhost:9090')

        async with httpx.AsyncClient(timeout=5.0) as client:
            # Query key cognitive metrics
            queries = {
                "active_cycles": "active_cognitive_cycles",
                "pipeline_completion": "pipeline_completion_rate",
                "cls_violations": "cls_preservation_violations_total",
                "phi3_bypasses": "phi3_bypass_attempts_total",
                "module_success_anterior": 'module_success_rate{module_name="anterior_helix"}',
                "module_success_posterior": 'module_success_rate{module_name="posterior_helix"}',
                "module_success_echostack": 'module_success_rate{module_name="echostack"}',
                "module_success_echoripple": 'module_success_rate{module_name="echoripple"}',
                "module_success_gyro": 'module_success_rate{module_name="gyro_harmonizer"}'
            }

            metrics_data = {}
            for metric_name, query in queries.items():
                try:
                    response = await client.get(f"{prometheus_url}/api/v1/query", params={"query": query})
                    if response.status_code == 200:
                        data = response.json()
                        if data["data"]["result"]:
                            value = float(data["data"]["result"][0]["value"][1])
                            metrics_data[metric_name] = value
                        else:
                            metrics_data[metric_name] = 0.0
                    else:
                        metrics_data[metric_name] = 0.0
                except Exception as e:
                    print(f"Failed to query {metric_name}: {e}")
                    metrics_data[metric_name] = 0.0

            # Add cognitive monitor data
            metrics_data.update({
                "active_cycles_count": len(cognitive_monitor.active_cycles),
                "total_cycles_completed": cognitive_monitor._get_total_cycles(),
                "avg_integrity_score": cognitive_monitor._calculate_avg_integrity()
            })

            return {
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics_data,
                "status": "healthy" if metrics_data.get("pipeline_completion", 0) > 0.8 else "warning"
            }

    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "status": "error"
        }

@app.get("/api/metrics/history")
async def get_metrics_history(hours: int = 24):
    """Get historical cognitive metrics"""
    try:
        prometheus_url = getattr(settings, 'prometheus_url', 'http://localhost:9090')

        # Calculate time range
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)

        async with httpx.AsyncClient(timeout=10.0) as client:
            # Query historical data for key metrics
            queries = [
                ("pipeline_completion", "pipeline_completion_rate"),
                ("active_cycles", "active_cognitive_cycles"),
                ("cls_violations", "increase(cls_preservation_violations_total[1h])")
            ]

            history_data = {}
            for metric_name, query in queries:
                try:
                    response = await client.get(
                        f"{prometheus_url}/api/v1/query_range",
                        params={
                            "query": query,
                            "start": int(start_time.timestamp()),
                            "end": int(end_time.timestamp()),
                            "step": "300"  # 5 minute intervals
                        }
                    )

                    if response.status_code == 200:
                        data = response.json()
                        if data["data"]["result"]:
                            # Extract time series data
                            values = data["data"]["result"][0]["values"]
                            history_data[metric_name] = [
                                {"timestamp": int(ts), "value": float(val)}
                                for ts, val in values
                            ]
                        else:
                            history_data[metric_name] = []
                    else:
                        history_data[metric_name] = []

                except Exception as e:
                    print(f"Failed to query history for {metric_name}: {e}")
                    history_data[metric_name] = []

            return {
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "history": history_data
            }

    except Exception as e:
        return {"error": str(e)}

@app.get("/api/cycles/active")
async def get_active_cycles():
    """Get details of currently active cognitive cycles"""
    active_cycles_data = []

    for cycle_id, metrics in cognitive_monitor.active_cycles.items():
        cycle_data = {
            "cycle_id": cycle_id,
            "entry_point": metrics.entry_point,
            "start_time": metrics.start_time,
            "duration": time.time() - metrics.start_time,
            "stages_completed": metrics.stages_completed,
            "module_metrics": metrics.module_metrics,
            "cls_violations": metrics.cls_violations,
            "integrity_score": metrics.final_integrity_score
        }
        active_cycles_data.append(cycle_data)

    return {
        "active_cycles": active_cycles_data,
        "total_active": len(active_cycles_data)
    }

@app.get("/api/alerts")
async def get_alerts():
    """Get current cognitive system alerts"""
    alerts = []

    # Check for critical issues
    if len(cognitive_monitor.active_cycles) > 10:
        alerts.append({
            "level": "warning",
            "message": "High number of active cognitive cycles",
            "value": len(cognitive_monitor.active_cycles),
            "threshold": 10
        })

    # Check module success rates
    for module_name, stats in cognitive_monitor.module_stats.items():
        if stats['total'] > 0:
            success_rate = stats['success'] / stats['total']
            if success_rate < 0.8:
                alerts.append({
                    "level": "error",
                    "message": f"Low success rate for {module_name}",
                    "value": success_rate,
                    "threshold": 0.8
                })

    # Check for CLS violations
    if cognitive_monitor._get_recent_cls_violations() > 5:
        alerts.append({
            "level": "critical",
            "message": "High CLS preservation violations detected",
            "value": cognitive_monitor._get_recent_cls_violations(),
            "threshold": 5
        })

    return {"alerts": alerts, "total": len(alerts)}

@app.post("/api/test/cognitive-cycle")
async def test_cognitive_cycle():
    """Trigger a test cognitive cycle for monitoring validation"""
    try:
        from cerebral_cortex.main import CortexRequest, BackgroundTasks

        test_request = CortexRequest(
            input_data="Test cognitive cycle for monitoring validation",
            context={"test_mode": True},
            priority="medium",
            source="monitoring_test"
        )

        # This would normally call process_request, but we'll simulate for testing
        cycle_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Start monitoring
        metrics = cognitive_monitor.start_cognitive_cycle(cycle_id, "monitoring_test")

        # Simulate pipeline stages
        await asyncio.sleep(0.1)  # Simulate preprocessing
        cognitive_monitor.complete_stage(cycle_id, cognitive_monitor.CognitiveStage.PREPROCESSING)

        await asyncio.sleep(0.2)  # Simulate module orchestration
        cognitive_monitor.complete_stage(cycle_id, cognitive_monitor.CognitiveStage.MODULE_ORCHESTRATION)

        # Simulate module executions
        cognitive_monitor.record_module_execution(cycle_id, "anterior_helix", 0.1, True)
        cognitive_monitor.record_module_execution(cycle_id, "posterior_helix", 0.15, True)
        cognitive_monitor.record_module_execution(cycle_id, "echostack", 0.12, True)

        await asyncio.sleep(0.3)  # Simulate harmonization
        cognitive_monitor.complete_stage(cycle_id, cognitive_monitor.CognitiveStage.HARMONIZATION)

        await asyncio.sleep(0.2)  # Simulate Phi-3 articulation
        cognitive_monitor.complete_stage(cycle_id, cognitive_monitor.CognitiveStage.PHI3_ARTICULATION)
        cognitive_monitor.record_phi3_interaction(cycle_id, "linguistic_articulation", 0.2)

        # Complete cycle
        cognitive_monitor.complete_stage(cycle_id, cognitive_monitor.CognitiveStage.OUTPUT_GENERATION)
        cognitive_monitor.complete_stage(cycle_id, cognitive_monitor.CognitiveStage.COMPLETE)
        cognitive_monitor.complete_cognitive_cycle(cycle_id, "success")

        return {
            "status": "test_completed",
            "cycle_id": cycle_id,
            "message": "Test cognitive cycle completed successfully"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Add helper methods to CognitiveMonitor
def _get_total_cycles(self):
    """Get total completed cycles (this would be tracked in a real implementation)"""
    return 42  # Placeholder

def _calculate_avg_integrity(self):
    """Calculate average integrity score"""
    if not self.active_cycles:
        return 1.0
    total_integrity = sum(metrics.final_integrity_score for metrics in self.active_cycles.values())
    return total_integrity / len(self.active_cycles)

def _get_recent_cls_violations(self):
    """Get count of recent CLS violations"""
    # This would track violations over time in a real implementation
    return 2  # Placeholder

# Methods are now implemented in the CognitiveMonitor class in telemetry.py

@app.get("/metrics")
async def prometheus_metrics():
    """Prometheus metrics endpoint for dashboard service"""
    metrics = []

    # Dashboard service metrics
    metrics.append("# HELP dashboard_uptime_seconds Time the dashboard has been running")
    metrics.append("# TYPE dashboard_uptime_seconds gauge")
    metrics.append(f"dashboard_uptime_seconds {time.time() - dashboard_cache['last_update']}")

    metrics.append("# HELP dashboard_requests_total Total requests served by dashboard")
    metrics.append("# TYPE dashboard_requests_total counter")
    metrics.append("dashboard_requests_total 0")  # Placeholder

    metrics.append("# HELP dashboard_active_connections Current active connections")
    metrics.append("# TYPE dashboard_active_connections gauge")
    metrics.append("dashboard_active_connections 0")  # Placeholder

    return "\n".join(metrics) + "\n"

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring dashboard"""
    return {
        "status": "healthy",
        "service": "cognitive_monitoring_dashboard",
        "timestamp": datetime.now().isoformat()
    }