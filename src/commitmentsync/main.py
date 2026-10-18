"""
CommitmentSync - Main API Application
Minimal viable implementation demonstrating core concept.
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

app = FastAPI(
    title="CommitmentSync",
    description="AI-driven, policy-centric engine for cross-cloud reservation optimization",
    version="0.1.0"
)


class HealthResponse(BaseModel):
    status: str
    version: str


class WorkloadData(BaseModel):
    cluster_id: str
    cpu_utilization: float
    memory_utilization: float
    storage_utilization: float
    hourly_cost: float


class RecommendationResponse(BaseModel):
    cluster_id: str
    recommended_reservation_type: str
    recommended_term_months: int
    estimated_savings_percent: float
    confidence_score: float


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to prove the app runs."""
    return HealthResponse(status="ok", version="0.1.0")


@app.post("/optimize", response_model=RecommendationResponse)
async def optimize_reservation(workload: WorkloadData):
    """
    Minimal reservation optimization endpoint.
    In a real implementation, this would use ML forecasting and policy evaluation.
    For now, returns a simple mock recommendation based on utilization.
    """
    # Simple mock logic: if utilization is high, recommend reserved instances
    avg_utilization = (workload.cpu_utilization + workload.memory_utilization + workload.storage_utilization) / 3
    
    if avg_utilization > 0.7:  # 70% utilization threshold
        recommended_type = "Standard Reserved Instance"
        term_months = 12
        savings_percent = 30.0
        confidence_score = 0.8
    elif avg_utilization > 0.4:  # 40% utilization threshold
        recommended_type = "Convertible Reserved Instance"
        term_months = 6
        savings_percent = 15.0
        confidence_score = 0.6
    else:
        recommended_type = "On-Demand (no reservation)"
        term_months = 0
        savings_percent = 0.0
        confidence_score = 0.9
    
    return RecommendationResponse(
        cluster_id=workload.cluster_id,
        recommended_reservation_type=recommended_type,
        recommended_term_months=term_months,
        estimated_savings_percent=savings_percent,
        confidence_score=confidence_score
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)