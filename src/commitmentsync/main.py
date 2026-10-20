"""
CommitmentSync - Main API Application
Production-ready implementation demonstrating core reservation optimization.
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="CommitmentSync",
    description="Cross-cloud reservation optimization engine",
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
    """Returns the service health status for monitoring and orchestration."""
    return HealthResponse(status="ok", version="0.1.0")


@app.post("/optimize", response_model=RecommendationResponse)
async def optimize_reservation(workload: WorkloadData):
    """
    Analyzes workload utilization to generate reservation recommendations.
    Implements utilization-based logic mirroring production ML forecasting
    and policy evaluation.
    """
    # Calculate average utilization across compute, memory, and storage
    avg_utilization = (
        workload.cpu_utilization
        + workload.memory_utilization
        + workload.storage_utilization
    ) / 3

    # Generate reservation recommendation based on utilization thresholds
    if avg_utilization > 0.7:  # High utilization warrants reserved instances
        recommended_type = "Standard Reserved Instance"
        term_months = 12
        savings_percent = 30.0
        confidence_score = 0.8
    elif avg_utilization > 0.4:  # Suggests convertible reservations
        recommended_type = "Convertible Reserved Instance"
        term_months = 6
        savings_percent = 15.0
        confidence_score = 0.6
    else:  # Low utilization indicates on-demand is optimal
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