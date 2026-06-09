from pathlib import Path
import fitz


def extract_pdf_metadata(
    file_path
):

    metadata = {}

    try:

        doc = fitz.open(
            file_path
        )

        page_count = len(
            doc
        )

        pdf_metadata = (
            doc.metadata
        )

        extracted_text = ""

        for page in doc:

            extracted_text += (
                page.get_text()
            )

        confidence = 1.0

        if len(
            extracted_text.strip()
        ) < 100:

            confidence = 0.4

        if len(
            extracted_text.strip()
        ) == 0:

            confidence = 0.1

        metadata = {

            "page_count":
            page_count,

            "file_size_kb":
            round(
                Path(
                    file_path
                ).stat().st_size
                / 1024,
                2
            ),

            "pdf_metadata":
            pdf_metadata,

            "ocr_confidence":
            confidence
        }

    except Exception:

        metadata = {

            "page_count": 0,

            "file_size_kb": 0,

            "pdf_metadata": {},

            "ocr_confidence": 0.0
        }
  
    metadata["producer"] = (

        metadata

        .get(

            "pdf_metadata",

            {}
        )

        .get(

            "producer"
        )
    )

    return metadata