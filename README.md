# Apple.com Automation Framework

Automated test framework for Apple.com built with Python, Playwright, and WebKit.

## Tech Stack
- Python 3.10
- Playwright (WebKit — Apple's open source Safari engine)
- pytest

## Test Coverage
- Homepage loading and navigation
- Mac, iPhone, iPad nav link routing
- Search — happy path, empty input, special characters

## Running Tests
```bash
pip install -r requirements.txt
playwright install webkit
pytest tests/ -v
```

## Structure
```
pages/          # Page Object Model classes
tests/          # Test suites
screenshots/    # Captured on each test run
```
