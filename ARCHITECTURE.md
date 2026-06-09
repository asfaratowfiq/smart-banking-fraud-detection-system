# Solution Architecture

## High Level Flow

```text
User Upload
    ↓
Streamlit UI
    ↓
FastAPI Backend
    ↓
Request Validation
    ↓
Celery Task Queue
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
Fraud Report Generation
    ↓
Streamlit Dashboard
```

---

# Components

## UI Layer

**Technology:** Streamlit

### Responsibilities

* Salary Slip upload
* Bank Statement upload
* Progress tracking
* Risk score visualization
* Fraud findings display
* AI risk summary display

---

## API Layer

**Technology:** FastAPI

### Responsibilities

* Request orchestration
* Workflow management
* Status tracking
* Result retrieval
* Integration with Celery workers

---

## Processing Layer

**Technology:** Celery + Redis

### Responsibilities

* Background task execution
* Asynchronous processing
* Workflow decoupling
* Scalability support

---

## OCR Layer

### Responsibilities

* PDF text extraction
* Structured data generation
* Salary slip parsing
* Bank statement parsing

---

## Metadata Analysis Layer

### Responsibilities

* PDF metadata extraction
* OCR confidence scoring
* Page count validation
* Producer information extraction
* Document quality analysis

---

## Normalization Layer

### Responsibilities

Convert extracted information into a standardized format.

### Examples

#### Salary Slip

```text
Net Salary
Gross Earnings
Total Deductions
Salary Month
```

#### Bank Statement

```text
Salary Credit
Opening Balance
Closing Balance
Total Credits
Total Debits
Statement Month
```

---

## Fraud Detection Layer

### Responsibilities

* Rule execution
* Single document validation
* Cross-document validation
* Fraud scoring

### Current Rules

#### Salary Rules

* SAL001 – Salary Missing
* SAL002 – Unusually High Salary
* SAL003 – Payroll Arithmetic Validation

#### Bank Rules

* DOC001 – Low Transaction Activity
* BANK001 – Balance Reconciliation Validation

#### Metadata Rules

* META001 – Low OCR Confidence
* META002 – Invalid Page Count
* META003 – Missing Producer Metadata

#### Cross Validation Rules

* CROSS001 – Salary Mismatch
* CROSS002 – Month Mismatch
* CROSS003 – Missing Salary Credit
* CROSS004 – Invalid Bank Statement
* CROSS005 – Invalid Salary Slip

#### Fraud Indicators

* FRAUD001 – High Salary Credit
* FRAUD002 – Excessive Transaction Volume

---

## AI Reasoning Layer

### Responsibilities

* Human-readable risk summary
* Fraud explanation
* Investigation recommendations
* Risk assessment narrative

---

# Current Architecture (Version 1.2)

```text
Streamlit
    ↓
FastAPI
    ↓
Celery + Redis
    ↓
OCR
    ↓
Metadata Analysis
    ↓
Normalization
    ↓
Fraud Detection Engine
       ├─ Salary Rules
       ├─ Bank Rules
       ├─ Metadata Rules
       └─ Cross Validation Rules
    ↓
AI Risk Assessment
    ↓
Fraud Report
```

---

# Future Architecture

## Phase 2

### Enhanced Validation

* SAL004 Amount-in-Words Validation
* SAL005 Statutory Deduction Validation
* BANK002 Transaction Sequence Validation
* BANK003 Salary Pattern Validation

### Authenticity Engine

* PDF Metadata Consistency Validation
* Digital Signature Validation
* PDF Tampering Detection
* OCR Layer Comparison

---

## Phase 3

### Intelligent Fraud Analytics

* Transaction Analytics Engine
* Behavioral Fraud Detection
* Historical Pattern Analysis
* AI Fraud Scoring Engine

---

## Phase 4

### Enterprise Capabilities

* Real-time Dashboard
* Audit Repository
* Case Management Workflow
* Investigation Tracking
* Compliance Reporting
