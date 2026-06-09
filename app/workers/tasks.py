from celery import chain
from pathlib import Path
import json

from app.services.normalization_service import normalize_text
from app.workers.celery_app import (
    celery_app
)

from app.services.status_service import (
    update_stage
)

from app.services.ocr_service import (
    extract_text_from_pdf
)

from app.services.metadata_service import (
    extract_pdf_metadata
)
from app.services.fraud_service import (
    apply_rules
)
from app.services.llm_service import (
    generate_reasoning
)

@celery_app.task
def ocr_task(
    request_id
):

    update_stage(
        request_id,
        "OCR",
        "PROCESSING"
    )

    request_folder = Path(
        f"temp_storage/{request_id}"
    )

    extracted_output = {}

    for file in request_folder.iterdir():

        if file.suffix.lower() == ".pdf":

            extracted_output[
                file.name
            ] = extract_text_from_pdf(
                file
            )

    with open(
        request_folder /
        "raw_extracted.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            extracted_output,
            f,
            indent=4
        )

    print(
        f"OCR completed -> {request_id}"
    )

    return request_id


@celery_app.task
def metadata_task(
    request_id
):

    update_stage(
        request_id,
        "METADATA",
        "PROCESSING"
    )

    request_folder = Path(
        f"temp_storage/{request_id}"
    )

    metadata_output = {}

    for file in request_folder.iterdir():

        if file.suffix.lower() == ".pdf":

            metadata_output[
                file.name
            ] = extract_pdf_metadata(
                file
            )

    with open(
        request_folder /
        "metadata.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata_output,
            f,
            indent=4
        )

    print(
        f"Metadata completed -> {request_id}"
    )

    return request_id



@celery_app.task
def normalization_task(
    request_id
):

    update_stage(

        request_id,

        "NORMALIZATION",

        "PROCESSING"
    )

    request_folder = Path(

        f"temp_storage/{request_id}"

    )

    with open(

        request_folder /
        "raw_extracted.json",

        "r",

        encoding="utf-8"

    ) as f:

        extracted_data = json.load(
            f
        )

    normalized_output = {}

    for file_name, text in extracted_data.items():

        normalized_output[
            file_name
        ] = normalize_text(
            text
        )

    with open(

        request_folder /
        "normalized_data.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            normalized_output,

            f,

            indent=4
        )

    print(

        f"Normalization completed -> {request_id}"

    )

    return request_id



@celery_app.task
def fraud_task(
    request_id
):

    update_stage(
        request_id,
        "FRAUD",
        "PROCESSING"
    )

    request_folder = Path(
        f"temp_storage/{request_id}"
    )

    with open(
    request_folder /
    "normalized_data.json",
    "r",
    encoding="utf-8"
) as f:

        normalized_data = json.load(
            f
        )

    with open(
        request_folder /
        "metadata.json",
        "r",
          encoding="utf-8"
    ) as f:

        metadata_data = json.load(
            f
        )

    result = apply_rules(
        normalized_data,
        metadata_data
    )

    reasoning = generate_reasoning(

        result,

        normalized_data,

        metadata_data
    )

    with open(

        request_folder /

        "reasoning.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            {

                "summary":

                reasoning
            },

            f,

            indent=4
        )

        with open(
            request_folder /
            "fraud_result.json",
            "w"
        ) as f:

            json.dump(
                result,
                f,
                indent=4
            )

        update_stage(
            request_id,
            "COMPLETED",
            "DONE"
        )

        print(
            f"Fraud completed -> {request_id}"
        )

        return request_id



def start_pipeline(
    request_id
):

    workflow = chain(

        ocr_task.s(
            request_id
        ),

        metadata_task.s(),

        normalization_task.s(),

        fraud_task.s()

    )

    workflow.delay()

