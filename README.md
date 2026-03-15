# Playwright Python E2E Automation Framework

A scalable and enterprise-ready **End-to-End Test Automation Framework** built using **Playwright, Pytest, and Python**.

The framework supports **UI, API, and Database validation within a unified automation architecture**, enabling reliable and maintainable testing for modern web applications. It is designed to support scalable automation suites and seamless CI/CD integration.

---

## Core Technologies

* Playwright
* Python
* Pytest
* Allure Reporting
* Pytest-xdist (Parallel Execution)

---

## Key Capabilities

* UI Automation using Playwright
* API Contract & Schema Validation
* Database Validation (MySQL)
* Data-Driven Testing (YAML / JSON)
* API Mocking / Network Interception
* Screenshot Capture on Failure
* Video Recording on Failure
* Allure Reporting Integration
* Failure Classification & Debug Capture
* Multi-Environment Execution
* Mobile Device Emulation
* Parallel Execution using pytest-xdist
* CI/CD Ready (Jenkins Compatible)

---

## Database Setup

Initialize the database before running tests:

```bash
mysql -u root -p < database/setup.sql
```

---

## Framework Architecture

```
playwright-e2e-framework/

config/          Environment configuration  
pages/           Page Object Model (POM)  
api_clients/     API abstraction layer  
db/              Database validation layer  
utils/           Reusable utilities  
schemas/         API schema definitions  
test_data/       YAML / JSON test data  
tests/           Test cases  
screenshots/     Failure screenshots  
videos/          Failure videos  
allure-results/  Raw Allure results
```

The framework follows clean architecture principles and separation of concerns to ensure maintainability and scalability.

---

## Installation & Setup

### Clone Repository

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

Environment configuration is managed through:

```
config/environments.yaml
```

Example configuration:

```yaml
dev:
  base_url: https://www.demoblaze.com
  api_url: https://api.demoblaze.com

  credentials:
    username: user
    password: pass
```

Run tests with a specific environment:

```bash
pytest --env=qa
```

---

## Device Execution (Desktop + Mobile)

Run default desktop execution:

```bash
pytest
```

Run tests on specific mobile devices:

```bash
pytest --ui-device="iPhone 13"
pytest --ui-device="Pixel 7"
pytest --ui-device="Galaxy S22"
```

Example combined execution:

```bash
pytest -m regression --env=qa --ui-device="iPhone 13"
```

---

## Marker-Based Execution

Smoke tests:

```bash
pytest -m smoke
```

Regression tests:

```bash
pytest -m regression
```

API tests:

```bash
pytest -m api
```

Contract tests:

```bash
pytest -m contract
```

Combined marker execution:

```bash
pytest -m "smoke or regression"
```

---

## Parallel Execution

Run tests in parallel:

```bash
pytest -n 2
```

Auto-detect CPU cores:

```bash
pytest -n auto
```

Example parallel execution:

```bash
pytest -m regression --env=qa --ui-device="Pixel 7" -n 2
```

---

## Allure Reporting

Serve report:

```bash
allure serve allure-results
```

Generate static report:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Reports include screenshots, videos, logs, and failure diagnostics.

---

## Failure Artifacts

On failure, the framework automatically captures:

* Screenshot
* Video recording
* Console logs
* Network failures
* Failure classification

Artifacts are stored in:

```
/screenshots
/videos/failures
```

These artifacts are also attached to **Allure reports** for easier debugging.

---

## CI/CD Integration

The framework supports integration with CI/CD pipelines such as Jenkins and enables:

* Parallel test execution
* Environment parameterization
* Device parameterization
* Automated Allure report generation

---

## Best Practices Implemented

* Page Object Model (POM)
* Separation of Concerns
* Contract Testing
* Data-Driven Testing
* Clean Test Design
* CLI-driven test execution
* Failure diagnostics and debugging support

---

## Framework Goals

* High test stability
* Scalable automation architecture
* Maintainable test suites
* Cross-device test coverage
* Enterprise-ready automation design

---
GitHub Repository:
https://github.com/qtpamit99/playwright-python-framework

## Author

**Amit Kumar Singh**
Senior QA Engineer | Test Automation | Playwright | API & Database Testing

If you find this framework useful, feel free to fork the repository and extend it.
