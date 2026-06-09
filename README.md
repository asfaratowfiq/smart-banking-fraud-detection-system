# Smart Banking Fraud Detection System

## Overview

Smart Banking Fraud Detection System is an AI-powered document verification platform designed to detect potential fraud indicators in Salary Slips and Bank Statements.

The solution combines:

* OCR-based document extraction
* Metadata analysis
* Data normalization
* Rule-based fraud detection
* AI-generated risk assessment summaries
* Interactive Streamlit dashboard

The system supports:

* Salary Slip Verification
* Bank Statement Verification
* Combined Verification

---

# Current Version

Version: 1.2

Status: Demo Ready

## Implemented Features

✓ Salary Slip Verification

✓ Bank Statement Verification

✓ Combined Verification

✓ Payroll Arithmetic Validation (SAL003)

✓ Balance Reconciliation Validation (BANK001)

✓ OCR Quality Validation

✓ Metadata Validation

✓ AI Risk Assessment

---

# Architecture

## High Level Flow

```text
User Upload
    ↓
Streamlit UI
    ↓
FastAPI Backend
    ↓
Celery Task Queue
    ↓
Redis Broker
    ↓
OCR Extraction
    ↓
Metadata Analysis
    ↓
Normalization Engine
    ↓
Fraud Detection Engine
    ↓
AI Risk Assessment
    ↓
Fraud Report
```

---

# Technology Stack

| Component             | Technology            |
| --------------------- | --------------------- |
| Frontend              | Streamlit             |
| Backend API           | FastAPI               |
| Background Processing | Celery                |
| Message Broker        | Redis                 |
| OCR Processing        | OCR Pipeline          |
| AI Reasoning          | OpenAI / Azure OpenAI |
| Language              | Python                |

---

# Fraud Detection Rules

## Salary Rules

| Rule ID | Description                   |
| ------- | ----------------------------- |
| SAL001  | Salary Missing                |
| SAL002  | Unusually High Salary         |
| SAL003  | Payroll Arithmetic Validation |

---

## Bank Rules

| Rule ID | Description                       |
| ------- | --------------------------------- |
| DOC001  | Low Transaction Activity          |
| BANK001 | Balance Reconciliation Validation |

---

## Metadata Rules

| Rule ID | Description               |
| ------- | ------------------------- |
| META001 | Low OCR Confidence        |
| META002 | Invalid Page Count        |
| META003 | Missing Producer Metadata |

---

## Cross Validation Rules

| Rule ID  | Description            |
| -------- | ---------------------- |
| CROSS001 | Salary Mismatch        |
| CROSS002 | Month Mismatch         |
| CROSS003 | Missing Salary Credit  |
| CROSS004 | Invalid Bank Statement |
| CROSS005 | Invalid Salary Slip    |

---

## Fraud Indicators

| Rule ID  | Description                  |
| -------- | ---------------------------- |
| FRAUD001 | High Salary Credit           |
| FRAUD002 | Excessive Transaction Volume |

---

# Project Structure

```text
smart-banking-fraud-detection-system/

├── app/
│   ├── api/
│   ├── services/
│   ├── workers/
│   ├── repositories/
│   └── models/
│
├── configs/
│   └── rules/
│
├── scripts/
│   └── start_all.bat
│
├── ui/
│
├── README.md
├── TESTING.md
└── FUTURE_ENHANCEMENTS.md
```

---

# Prerequisites

Install the following:

* Python 3.11+
* Redis Server
* Git

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd smart-banking-fraud-detection-system
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

---

## Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

## Start Redis

Ensure Redis is installed and running.

Example:

```bash
redis-server
```

---

## Start Complete Application

The project includes a startup script:

```bash
scripts\start_all.bat
```

This script automatically starts:

* FastAPI Backend
* Celery Worker
* Streamlit UI

---

# Access Application

## Streamlit UI

```text
http://localhost:8501
```

---

## FastAPI Swagger Documentation

```text
http://localhost:8000/docs
```

---

# Supported Analysis Types

## Salary Slip Verification

Validates:

* Salary extraction
* Salary consistency
* Payroll arithmetic

Required Document:

* Salary Slip PDF

---

## Bank Statement Verification

Validates:

* Salary credit extraction
* Transaction activity
* Balance reconciliation

Required Document:

* Bank Statement PDF

---

## Combined Verification

Validates:

* Salary amount matching
* Salary month matching
* Salary credit verification
* Cross-document consistency

Required Documents:

* Salary Slip PDF
* Bank Statement PDF

---

# Testing

All planned proof-of-concept scenarios have been successfully validated.

Refer:

```text
TESTING.md
```

for detailed testing evidence.

---

# Future Enhancements

Refer:

```text
FUTURE_ENHANCEMENTS.md
```

for the product roadmap and future capabilities.

---

# Docker Support

Docker is currently not required.

The application can be executed directly using:

* Python
* Redis
* FastAPI
* Celery
* Streamlit

Future releases may include:

* Docker
* Docker Compose
* Containerized Deployment

---

# Limitations

Current version does not perform:

* PDF tampering detection
* Digital signature validation
* Amount-in-words validation
* Statutory deduction validation
* Multi-month trend analysis

These capabilities are planned for future releases.

---

# License

Internal Proof of Concept (POC)

Developed for learning, experimentation, and demonstration purposes.
