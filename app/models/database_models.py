"""SQLAlchemy ORM models for Project Fifty."""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


class User(Base):
    """System user model."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="analyst")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    analysis_requests = relationship("AnalysisRequest", back_populates="user")


class Location(Base):
    """Geographic location model for Rwanda's sectors."""

    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False, index=True)
    province = Column(String(100))
    district = Column(String(100))
    sector = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    population = Column(Integer)
    area_km2 = Column(Float)
    metadata_ = Column("metadata", JSON, default=dict)

    analysis_requests = relationship("AnalysisRequest", back_populates="location")


class AnalysisRequest(Base):
    """Records of user analysis requests."""

    __tablename__ = "analysis_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True)
    location_name = Column(String(200), nullable=False)
    query = Column(Text, nullable=False)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    result_summary = Column(Text)
    risk_level = Column(String(50))
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="analysis_requests")
    location = relationship("Location", back_populates="analysis_requests")
    agent_results = relationship("AgentResult", back_populates="analysis_request")
    reports = relationship("ClimateReport", back_populates="analysis_request")


class AgentResult(Base):
    """Stores individual agent execution results."""

    __tablename__ = "agent_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    analysis_request_id = Column(
        UUID(as_uuid=True),
        ForeignKey("analysis_requests.id"),
        nullable=False,
    )
    agent_name = Column(String(200), nullable=False)
    agent_role = Column(String(200))
    task_description = Column(Text)
    output = Column(Text)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    execution_time_ms = Column(Integer)
    confidence_score = Column(Float)
    metadata_ = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis_request = relationship("AnalysisRequest", back_populates="agent_results")


class ClimateReport(Base):
    """Final generated climate intelligence reports."""

    __tablename__ = "climate_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    analysis_request_id = Column(
        UUID(as_uuid=True),
        ForeignKey("analysis_requests.id"),
        nullable=False,
    )
    title = Column(String(500))
    summary = Column(Text)
    risk_level = Column(String(50))
    confidence = Column(Float)
    recommendations = Column(JSON, default=list)
    full_report = Column(Text)
    format_type = Column(String(50), default="json")  # json, markdown, pdf
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis_request = relationship("AnalysisRequest", back_populates="reports")
