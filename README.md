# Accessibility Testing Automation Framework
A professional, enterprise-grade accessibility testing framework based on **Playwright + Axe + POM** design pattern.

## Features
✅ Page Object Model (POM)
✅ wcag2a | wcag2aa | wcag21a | wcag21aa | section508 | EN-301-549
✅ allure support

## Quick Start
```bash
pip install -r requirements.txt
playwright install

How to add a new one
1. Create a new config file under config folder and update __init__.py file

2. Create the new folder/files under pages

3. Create the new folder/files under tests


How to Run
1. Use command "pytest tests/saucedemo/ -v --env saucedemo" and check reports under report folder 
2. use command "allure open allure-report" if you want to check allure report  