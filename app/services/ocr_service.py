import fitz
import pdfplumber


def extract_text_from_pdf(
    pdf_path
):

    extracted_text = ""

    try:

        with pdfplumber.open(
            pdf_path
        ) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:

                    extracted_text += (
                        text + "\n"
                    )

    except Exception:

        doc = fitz.open(
            pdf_path
        )

        for page in doc:

            extracted_text += (
                page.get_text()
            )

    return extracted_text