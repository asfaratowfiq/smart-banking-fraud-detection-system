from app.db.session import SessionLocal
from app.models.analysis_request import (
    AnalysisRequest
)


def create_request(
    request_id,
    analysis_type
):

    db = SessionLocal()

    try:

        record = AnalysisRequest(

            request_id=request_id,

            analysis_type=analysis_type,

            status="UPLOADED",

            current_stage="UPLOAD"
        )

        db.add(record)

        db.commit()

    finally:

        db.close()
