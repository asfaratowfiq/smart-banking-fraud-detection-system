from pathlib import Path
import shutil


def save_uploaded_file(
    file,
    request_folder
):

    file_path = (
        request_folder /
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return str(file_path)