
import streamlit as st
import requests
import time

API_BASE = "http://127.0.0.1:8000/api/v1"

st.set_page_config(

    page_title="Smart Banking Fraud Detection",

    layout="wide"
)

st.title(

    "🏦 Smart Banking Fraud Detection System"
)

st.info(

        "AI-powered Salary Slip & Bank Statement Verification"
)

analysis_type_display = st.selectbox(

    "Choose Verification Mode",

    [

        "Salary Slip Verification",

        "Bank Statement Verification",

        "Combined Verification"
    ]
)

analysis_type_map = {

    "Salary Slip Verification": "salary_only",

    "Bank Statement Verification": "bank_only",

    "Combined Verification": "combined"
}

analysis_type = analysis_type_map[

    analysis_type_display
]

salary_file = None
bank_file = None

# -------------------------
# Upload Section
# -------------------------

if analysis_type == "salary_only":

    salary_file = st.file_uploader(

        "📄 Upload Salary Slip",

        type=["pdf"],

        key="salary"
    )

elif analysis_type == "bank_only":

    bank_file = st.file_uploader(

       "🏦 Upload Bank Statement",

        type=["pdf"],

        key="bank"
    )

else:

    col1, col2 = st.columns(2)

    with col1:

        salary_file = st.file_uploader(

            "Upload Salary Slip",

            type=["pdf"],

            key="salary_combined"
        )

    with col2:

        bank_file = st.file_uploader(

           "Upload Bank Statement",

            type=["pdf"],

            key="bank_combined"
        )

# -------------------------
# Validation
# -------------------------

disable_button = False

if analysis_type == "salary_only":

    disable_button = salary_file is None

elif analysis_type == "bank_only":

    disable_button = bank_file is None

else:

    disable_button = (

        salary_file is None

        or

        bank_file is None
    )

# -------------------------
# Analysis Button
# -------------------------

if st.button(

    "Analyze Documents",

    disabled=disable_button
):

    files = {}

    data = {

        "analysis_type":

        analysis_type
    }

    if salary_file:

        files["salary_slip"] = (

            salary_file.name,

            salary_file,

            "application/pdf"
        )

    if bank_file:

        files["bank_statement"] = (

            bank_file.name,

            bank_file,

            "application/pdf"
        )

    response = requests.post(

        f"{API_BASE}/analyze",

        data=data,

        files=files
    )

    result = response.json()

    if response.status_code != 200:

        st.error(

            f"API Error: {result}"
        )

        st.stop()

    request_id = result.get(

        "request_id"
    )

    st.success(

        f"Analysis Request ID: {request_id}"
    )

    st.divider()

    progress = st.progress(0)

    status_box = st.empty()

    stage_map = {

        "UPLOAD": 10,

        "OCR": 25,

        "METADATA": 50,

        "NORMALIZATION": 75,

        "FRAUD": 90,

        "COMPLETED": 100
    }

    while True:

        status = requests.get(

            f"{API_BASE}/status/{request_id}"

        ).json()

        stage = status.get(

            "stage",

            ""
        )

        progress.progress(

            stage_map.get(

                stage,

                0
            )
        )

        stage_display = {

            "UPLOAD": "Document Upload",

            "OCR": "Text Extraction",

            "METADATA": "Metadata Analysis",

            "NORMALIZATION": "Data Processing",

            "FRAUD": "Fraud Assessment",

            "COMPLETED": "Completed"
            }

        status_box.info(

            f"Current Stage: {stage_display.get(stage, stage)}"
        )

        if status.get(

            "status"

        ) == "DONE":

            break

        time.sleep(2)

    result_data = requests.get(

        f"{API_BASE}/result/{request_id}"

    ).json()

    fraud = result_data.get(

        "fraud_result",

        {}
    )

    metadata = result_data.get(

        "metadata",

        {}
    )

    normalized = result_data.get(

        "normalized_data",

        {}
    )

    score = fraud.get(

        "score",

        0
    )

    if score < 20:

        risk = "LOW"

    elif score < 50:

        risk = "MEDIUM"

    else:

        risk = "HIGH"

    st.success(

        "Analysis Completed"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Risk Score",

            score
        )

    with col2:

        st.metric(

            "Risk Level",

            risk
        )

    # -------------------------
    # Document Analysis
    # -------------------------

    st.subheader(

        "Document Analysis"
    )

    for file_name, values in normalized.items():

        meta = metadata.get(

            file_name,

            {}
        )

        document_type = values.get(

            "document_type",

            ""
        )

        if document_type == "salary_slip":

            st.markdown(
                "### 📄 Salary Slip"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Net Salary",
                    values.get(
                        "net_salary",
                        "N/A"
                    )
                )

            with col2:

                st.metric(
                    "Salary Month",
                    values.get(
                        "salary_month",
                        "N/A"
                    )
                )

            with col3:

                st.metric(
                    "OCR Confidence (Text Extraction Quality or Document Quality)",
                    meta.get(
                        "ocr_confidence",
                        "N/A"
                    )
                )

            with col4:

                st.metric(
                    "Pages",
                    meta.get(
                        "page_count",
                        "N/A"
                    )
                )

        elif document_type == "bank_statement":

            st.markdown(
                "### 🏦 Bank Statement"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Salary Credit",
                    values.get(
                        "salary_credit_amount",
                        "N/A"
                    )
                )

            with col2:

                st.metric(
                    "Statement Month",
                    values.get(
                        "statement_month",
                        "N/A"
                    )
                )

            with col3:

                st.metric(
                    "OCR Confidence (Text Extraction Quality)",
                    meta.get(
                        "ocr_confidence",
                        "N/A"
                    )
                )

            with col4:

                st.metric(
                    "Pages",
                    meta.get(
                        "page_count",
                        "N/A"
                    )
                )

        st.divider()


    # -------------------------
    # Fraud Findings
    # -------------------------

    st.subheader(

        "Fraud Findings"
    )

    findings = fraud.get(

        "findings",

        []
    )

    if findings:

        st.info(

            f"{len(findings)} risk indicator(s) detected"
        )

        for finding in findings:

            title = (

                f"{finding['rule_id']}"

                f" | "

                f"{finding['severity']}"
            )

            with st.expander(

                title,

                expanded=False
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(

                        "**Rule ID:**",

                        finding["rule_id"]
                    )

                with col2:

                    st.write(

                        "**Severity:**",

                        finding["severity"]
                    )

                st.write(

                    "**Description:**",

                    finding["message"]
                )

    else:

        st.success(

            "✓ No risk indicators detected"
        )

    # -------------------------
    # AI Summary
    # -------------------------

    st.subheader(

        "Risk Assessment Summary"
    )

    reasoning = result_data.get(

        "reasoning",

        {}
    )

    summary = reasoning.get(

        "summary",

        "No AI reasoning available"
    )

    st.info(

        summary
    )

# -------------------------
# Help Section
# -------------------------

with st.expander(

    "How To Interpret Results"
):

    st.markdown("""

**Fraud Score**

- 0 - 19 → Low Risk  
- 20 - 49 → Medium Risk  
- 50+ → High Risk  

**OCR Confidence (Text Extraction Quality or Document Quality)**

- 0.90 - 1.00 → Excellent  
- 0.70 - 0.89 → Acceptable  
- Below 0.70 → Review Required  

**Salary = N/A**

- Salary extraction failed  

**Page Count = 0**

- Possible extraction issue  

""")
