from fastapi import APIRouter

from app.db.session import (
    SessionLocal
)

from app.models.analysis_request import (
    AnalysisRequest
)

router = APIRouter()


@router.get(
    "/status/{request_id}"
)
def get_status(
    request_id
):

    db = SessionLocal()

    try:

        record = (

            db.query(
                AnalysisRequest
            )

            .filter(
                AnalysisRequest.request_id
                == request_id
            )

            .first()
        )

        if not record:

            return {

                "message":
                "Request not found"
            }

        return {

            "request_id":
            record.request_id,

            "status":
            record.status,

            "stage":
            record.current_stage
        }

    finally:

        db.close()