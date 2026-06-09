from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class AnalysisRequest(Base):
    __tablename__ = "analysis_requests"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(
        String,
        unique=True,
        nullable=False
    )

    analysis_type = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    current_stage = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )