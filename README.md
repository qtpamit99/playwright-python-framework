# Playwright E2E Automation Framework

A scalable, environment-driven, and enterprise-ready automation framework built using:

- Playwright
- Pytest
- Python
- UI + API + Database Validation
- Allure Reporting
- Parallel Execution
- Mobile Device Emulation
- Failure Intelligence

---

## Key Capabilities

- UI Automation (Playwright)
- API Contract Validation
- Database Validation (MySQL)
- Schema Validation
- Data-Driven Testing (YAML / JSON)
- API Mocking / Interception
- Screenshot on Failure
- Video Recording (Failure Only)
- Allure Reporting
- Failure Classification & Debug Capture
- Multi-Environment Execution
- Dynamic Mobile Device Emulation
- Parallel Execution (pytest-xdist)
- CI/CD Ready (Jenkins Compatible)

---

## Framework Architecture

playwright-e2e-framework/

config/              Environment configuration  
pages/               Page Object Model (POM)  
api_clients/         API abstraction layer  
db/                  Database layer  
utils/               Reusable utilities  
schemas/             API schema definitions  
test_data/           YAML / JSON test data  
tests/               Test cases  
screenshots/         Failure screenshots  
videos/              Failure videos  
allure-results/      Raw Allure results  

---

## Installation & Setup

### Clone Project

```bash
git clone <repository-url>
cd playwright-e2e-framework
```

### Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright Browsers

```bash
playwright install
```

---

## Environment Configuration

Environment details are managed via:

config/environments.yaml

Example:

```yaml
dev:
  base_url: https://www.demoblaze.com/
  api_url: https://api.demoblaze.com

  credentials:
    username: user
    password: pass
```

Run with specific environment:

```bash
pytest --env=qa
```

---

## Device Execution (Desktop + Mobile)

The framework supports real mobile emulation using Playwright device profiles.

### Desktop (Default)

```bash
pytest
```

### Run on Specific Device

```bash
pytest --ui-device="iPhone 13"
pytest --ui-device="Pixel 7"
pytest --ui-device="Galaxy S22"
```

### Combined Example

```bash
pytest -m regression --env=qa --ui-device="iPhone 13"
```

---

## Marker-Based Execution

### Smoke

```bash
pytest -m smoke
```

### Regression

```bash
pytest -m regression
```

### API Tests

```bash
pytest -m api
```

### Contract Tests

```bash
pytest -m contract
```

### Combined

```bash
pytest -m "smoke or regression"
```

---

## Parallel Execution

```bash
pytest -n 2
pytest -n auto
```

Example:

```bash
pytest -m regression --env=qa --ui-device="Pixel 7" -n 2
```

---

## Allure Reporting

### Generate & Serve

```bash
allure serve allure-results
```

### Generate Static Report

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

---

## Artifacts

On failure, the framework automatically captures:

- Screenshot
- Video (failure only)
- Console logs
- Network failures
- Failure classification

Stored in:

/screenshots  
/videos/failures  

Artifacts are also attached inside Allure reports.

---

## CI/CD Ready

The framework supports:

- Jenkins Pipeline
- Parallel execution
- Environment parameterization
- Device parameterization
- Allure integration

---

## Best Practices Followed

- Page Object Model
- Separation of Concerns
- Contract Testing
- Data-Driven Testing
- Failure Diagnostics
- Clean Test Design
- CLI-driven execution

---

## Framework Goals

- Stability
- Scalability
- Maintainability
- Cross-device coverage
- Enterprise-ready architecture