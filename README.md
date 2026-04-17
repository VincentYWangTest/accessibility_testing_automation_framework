# Accessibility Testing Automation Framework
A professional, enterprise-grade accessibility testing framework based on **Playwright + Axe + POM** design pattern.

## Features
✅ Page Object Model (POM)
✅ Multi-environment support
✅ WCAG 2.1 AA Compliance
✅ 5 types of reports: HTML, PDF, CSV, JSON, Allure
✅ Critical severity filter
✅ Auto screenshot & logging
✅ Windows/macOS compatible

## Quick Start
```bash
pip install -r requirements.txt
playwright install
python run.py

How to Add a New Test Site / New Case
1. Add a New Environment Config (Optional)
Create a new config file in config/ or add directly to the existing config:

2. Create a New Test File
Copy one of the existing test files in the tests/ folder, e.g.:
tests/test_new_site.py
