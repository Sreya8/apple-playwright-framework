# Apple.com Automation Framework

Automated test framework for Apple.com built with Python, Playwright, and WebKit.

## Tech Stack
- Python 3.10
- Playwright (WebKit - Apple's open source Safari engine)
- pytest

## Test Coverage
- Homepage loading and navigation
- Mac, iPhone, iPad nav link routing
- Search: happy path, empty input, special characters

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

## Findings

### Finding 1 — HTTP 400 on Special Character Search
**Test:** `test_search_special_characters`  
**Input:** `!@#$%`  
**Both WebKit and Chromium:** HTTP 400 "Ambiguous URI path encoding"  
**URL:** `https://www.apple.com/us/search/!%40%23%24%25?src=globalnav`  
**Root cause:** Apple's server rejects the URI-encoded form of `!@#$%`  
**Severity:** Medium — affects any user searching with these characters  
**Expected:** Graceful "no results" page or sanitized search  
**Actual:** Raw HTTP 400 error page shown to user
