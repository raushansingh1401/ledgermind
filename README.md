# LedgerMind

AI-powered transaction auto-tagging and finance operations assistant.

## Overview

LedgerMind is an intelligent finance workflow system designed to accelerate month-end close by automatically classifying transactions into accounting categories.

The system combines:

* Rule-based transaction classification
* LLM-powered vendor understanding (Google Gemini)
* Human-in-the-loop review workflows
* Continuous learning from accountant feedback

The project was inspired by real-world finance operations challenges where manual transaction coding consumes significant time during the monthly close process.

---

## Problem Statement

Finance teams process hundreds of transactions every month.

Each transaction must be mapped to the correct accounting category before it can be posted to the accounting system.

Examples:

| Vendor | Accounting Category  |
| ------ | -------------------- |
| AWS    | Cloud Infrastructure |
| Notion | SaaS Tools           |
| Uber   | Travel Expense       |

Manual classification creates several challenges:

* Time-consuming month-end close
* Inconsistent coding
* High operational overhead
* Long-tail vendors that are difficult to classify

LedgerMind addresses these challenges through intelligent automation while preserving human oversight.

---

## Key Features

### Transaction Ingestion

Transactions can be submitted through REST APIs.

Example:

```json
{
  "vendor": "Figma",
  "description": "Design collaboration software",
  "amount": 120,
  "currency": "USD"
}
```

---

### Vendor Rule Engine

Previously reviewed vendors are stored as reusable classification rules.

Example:

```text
AWS → Cloud Infrastructure
Notion Labs → SaaS Tools
```

Known vendors are classified instantly without requiring LLM inference.

---

### LLM-Powered Classification

When no historical vendor rule exists, LedgerMind uses Google Gemini to infer the most likely accounting category.

Example:

```text
Vendor: Figma
Description: Design collaboration software

Suggested Category: SaaS Tools
Confidence: 0.99
```

---

### Confidence-Based Decision Routing

LedgerMind never blindly trusts AI outputs.

High-confidence classifications:

```text
AUTO_POSTED
```

Lower-confidence classifications:

```text
PENDING_REVIEW
```

This design minimizes silent miscoding, which is critical in financial systems.

---

### Human-in-the-Loop Learning

Accountants can review and correct classifications.

Example:

```text
Linear
↓
Corrected to SaaS Tools
↓
Vendor Rule Created
↓
Future transactions auto-classified
```

This creates a continuous learning loop.

---

## System Architecture

```text
Transaction
      │
      ▼
Vendor Rule Lookup
      │
      ├── Match Found
      │       ▼
      │   AUTO_POSTED
      │
      └── No Match
              ▼
        Gemini Classification
              ▼
        Confidence Evaluation
              ▼
      ┌───────────────┐
      │ Confidence >= Threshold │
      └───────────────┘
          │               │
          ▼               ▼
    AUTO_POSTED    PENDING_REVIEW
                          │
                          ▼
                  Accountant Feedback
                          ▼
                    Vendor Rule Update
```

---

## Tech Stack

### Backend

* FastAPI
* Python

### Database

* SQLite
* SQLAlchemy ORM

### AI

* Google Gemini API

### Tooling

* Git
* GitHub
* VS Code

---

## API Endpoints

### Create Transaction

```http
POST /transactions
```

Creates and classifies a transaction.

---

### Submit Feedback

```http
POST /feedback
```

Stores accountant corrections and updates vendor learning rules.

---

### Seed Demo Rules

```http
GET /seed-rules
```

Populates sample vendor mappings.

---

## Future Improvements

* Multi-tenant chart of accounts
* Retrieval-augmented vendor memory
* Evaluation framework for classification accuracy
* Audit trails and approval workflows
* Accounting platform integrations
* Multi-currency support
* Explainability and reasoning traces
* Transaction batch processing

---

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment file:

```env
GEMINI_API_KEY=<your_api_key>
```

Start the server:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Author

Raushan Singh

AI-powered finance automation project demonstrating agentic workflows, human-in-the-loop learning, and intelligent transaction classification.
