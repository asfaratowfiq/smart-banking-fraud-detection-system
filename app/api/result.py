from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter()


@router.get(
    "/result/{request_id}"
)
def get_result(
    request_id
):

    request_folder = Path(
        f"temp_storage/{request_id}"
    )

    if not request_folder.exists():

        return {

            "message":
            "Request not found"
        }

    response = {}

    files_to_load = [

        "metadata.json",

        "normalized_data.json",

        "fraud_result.json",
        
        "reasoning.json"

    ]

    for file_name in files_to_load:

        file_path = (

            request_folder /
            file_name
        )

        if file_path.exists():

            with open(

                file_path,

                "r",

                encoding="utf-8"

            ) as f:

                response[
                    file_name.replace(
                        ".json",
                        ""
                    )
                ] = json.load(
                    f
                )

    return response
