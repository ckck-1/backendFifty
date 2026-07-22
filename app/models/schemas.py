"""Pydantic schemas for request/response validation."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── Request Schemas ──────────────────────────────────────────────

class AnalysisRequest(BaseModel):
    """Schema for submitting a climate analysis request."""
    location: str = Field(..., description="Rwanda sector or district name", examples=["Bugesera"])
    query: str = Field(..., description="Natural language analysis query", examples=["Analyze drought risk"])


class LocationCreate(BaseModel):
    """Schema for creating a location record."""
    name: str
    province: Optional[str] = None
    district: Optional[str] = None
    sector: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: Optional[int] = None
    area_km2: Optional[float] = None


# ── Response Schemas ─────────────────────────────────────────────

class AgentInfo(BaseModel):
    """Public info about a registered agent."""
    name: str
    role: str
    goal: str
    tools: list[str]


class AgentExecutionDetail(BaseModel):
    """Detail for one agent's execution within an analysis."""
    agent_name: str
    output: str
    status: str
    execution_time_ms: Optional[int] = None
    confidence_score: Optional[float] = None


class AnalysisResponse(BaseModel):
    """Schema returned after a completed analysis."""
    location: str
    risk_level: str
    confidence: str
    analysis: str
    recommendations: list[str] = Field(default_factory=list)


class DetailedAnalysisResponse(BaseModel):
    """Extended analysis response with agent-level detail."""
    request_id: UUID
    location: str
    query: str
    status: str
    risk_level: Optional[str] = None
    confidence: Optional[float] = None
    summary: Optional[str] = None
    recommendations: list[str] = Field(default_factory=list)
    agent_results: list[AgentExecutionDetail] = Field(default_factory=list)
    created_at: datetime
    completed_at: Optional[datetime] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    project: str
    version: str
    database: str = "connected"
    agents_registered: int


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    code: str = "INTERNAL_ERROR"
