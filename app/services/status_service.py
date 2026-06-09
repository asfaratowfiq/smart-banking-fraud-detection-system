from app.db.session import (
    SessionLocal
)

from app.models.analysis_request import (
    AnalysisRequest
)


def update_stage(
    request_id,
    stage,
    status
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

        if record:

            record.current_stage = stage

            record.status = status

            db.commit()

    finally:

        db.close()
