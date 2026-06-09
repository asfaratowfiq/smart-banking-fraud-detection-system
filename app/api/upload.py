from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException
)

from pathlib import Path
import uuid

from app.services.storage_service import (
    save_uploaded_file
)

from app.services.request_service import (
    create_request
)
from app.workers.tasks import (
    start_pipeline
)

router = APIRouter()


@router.post("/analyze")
def analyze(
    analysis_type: str = Form(...),
    salary_slip: UploadFile = File(None),
    bank_statement: UploadFile = File(None)
):

    # ----------------------------
    # Validate analysis type
    # ----------------------------

    allowed_types = [
        "salary_only",
        "bank_only",
        "combined"
    ]

    if analysis_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail="Invalid analysis type"
        )

    # ----------------------------
    # Validate files
    # ----------------------------

    if analysis_type == "salary_only":

        if not salary_slip:

            raise HTTPException(
                status_code=400,
                detail="Salary slip required"
            )

    elif analysis_type == "bank_only":

        if not bank_statement:

            raise HTTPException(
                status_code=400,
                detail="Bank statement required"
            )

    elif analysis_type == "combined":

        if not salary_slip or not bank_statement:

            raise HTTPException(
                status_code=400,
                detail="Both files required"
            )

    # ----------------------------
    # Generate Request ID
    # ----------------------------

    request_id = f"REQ_{uuid.uuid4().hex[:8]}"

    # ----------------------------
    # Create Temp Folder
    # ----------------------------

    request_folder = Path(
        f"temp_storage/{request_id}"
    )

    request_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # ----------------------------
    # Save Salary Slip
    # ----------------------------

    if salary_slip:

        save_uploaded_file(
            salary_slip,
            request_folder
        )

    # ----------------------------
    # Save Bank Statement
    # ----------------------------

    if bank_statement:

        save_uploaded_file(
            bank_statement,
            request_folder
        )

    # ----------------------------
    # Save Request Record
    # ----------------------------

    create_request(
        request_id,
        analysis_type
    )

    # ----------------------------
    # Future Worker Trigger
    # ----------------------------
    print(
    f"Starting pipeline for {request_id}"
)
    start_pipeline(
        request_id
    )
    return {

        "request_id": request_id,

        "status": "UPLOADED"
    }

