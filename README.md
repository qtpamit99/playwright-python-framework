# Playwright E2E Framework (Python + Pytest)

A scalable, maintainable, and contract-driven automation framework built using:

- Playwright  
- Pytest  
- Python  
- UI + API + DB Validation  
- Allure Reporting  
- Failure Intelligence  

---

# Framework Highlights

- UI Automation (Playwright)  
- API Contract Validation  
- Database Validation (MySQL)  
- Schema Validation  
- Data-Driven Testing  
- Mocking / API Interception  
- Screenshot & Video Capture  
- Allure Reporting  
- Smart Failure Analysis  

---

# Framework Architecture

playwright-e2e-framework/

- config/              → Environment configuration  
- pages/               → Page Object Model (POM)  
- api_clients/         → API abstraction layer  
- db/                  → Database layer  
- utils/               → Reusable utilities  
- schemas/             → API schema definitions  
- test_data/           → YAML / JSON test data  
- tests/               → Test cases  
- screenshots/         → Failure screenshots  
- videos/              → Failure videos  
- allure-results/      → Raw Allure results  

---

# Installation & Setup

## Clone Project

```bash
git clone <repo-url>
cd playwright-e2e-framework
```

---

## Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Playwright Browsers

```bash
playwright install
```

---

# Allure Reporting Setup

## Install Allure CLI

Using Scoop (Recommended for Windows):

```bash
scoop install allure
```

Verify:

```bash
allure --version
```

---

# Test Execution

## Run All Tests

```bash
pytest
```

---

## Run Environment-Specific Tests

```bash
pytest --env=dev
pytest --env=qa
```

---

## Run By Marker

### Smoke Tests

```bash
pytest -m smoke
```

---

### Regression Tests

```bash
pytest -m regression
```

---

### Contract Tests

```bash
pytest -m contract
```

---

### API Tests

```bash
pytest -m api
```

---

### Combined Execution

```bash
pytest -m "smoke or regression"
pytest -m "regression and not api"
```

---

# Allure Report Generation

## Serve Report

```bash
allure serve allure-results
```

This command generates the report and opens it in the browser.

---

## Generate Static Report

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Useful for CI/CD pipelines.

---

# Artifacts & Debugging

The framework automatically captures:

- Screenshot on failure  
- Video on failure  

Artifacts are stored in:

- /screenshots  
- /videos/failures  

Artifacts are also attached inside Allure reports.

---

# Failure Intelligence Features

- Failure Classification  
- Page State Capture  
- Logs & Debug Information  

These features assist in faster root cause analysis.

---

# Environment Configuration

Environment data is managed via:

config/environments.yaml

Example:

```yaml
dev:
  base_url: https://example.com
  api_url: https://api.example.com

  credentials:
    username: testuser
    password: secret
```

Run tests using:

```bash
pytest --env=dev
```

---

# Test Design Philosophy

- Clean Test Files  
- Reusable Utilities  
- Strict Contract Validation  
- No Duplicate Logic  
- POM-Centric UI Tests  

---

# Best Practices Followed

- Page Object Model (POM)  
- Separation of Concerns  
- Contract Testing  
- Data-Driven Testing  
- Failure Diagnostics  

---

# Troubleshooting

## Allure Command Not Found

Verify installation:

```bash
allure --version
```

---

## Playwright Browser Issues

Reinstall browsers:

```bash
playwright install
```

---

## Tests Not Running With Marker

Ensure the test is tagged:

```python
@pytest.mark.smoke
```

---

# Framework Goals

- Stability  
- Scalability  
- Maintainability  
- Enterprise-Ready Design  