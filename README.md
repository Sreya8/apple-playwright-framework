# Apple.com Automation Framework

A production-style test automation framework targeting live Apple.com, 
built with Python, Playwright, and WebKit — Apple's open source Safari engine.

## Tech Stack
- **Python 3.10**
- **Playwright** — browser automation with WebKit and Chromium
- **pytest** — test runner and fixture management
- **WebKit** — Apple's open source Safari engine (same engine powering Safari, 
  Mail, and App Store on macOS/iOS)

## Structure
```
pages/                  # Page Object Model classes
├── homepage.py         # Nav, search trigger, homepage assertions
├── searchpage.py       # Search flow, edge cases
└── product_page.py     # MacBook Air — heading, price, buy button
tests/                  # Test suites mirroring page structure
├── test_homepage.py
├── test_search.py
└── test_product.py
conftest.py             # Browser fixtures and configuration
screenshots/            # Captured on every test run
```

## Running Tests
```bash
pip install -r requirements.txt
playwright install webkit
pytest tests/ -v
```

Cross-browser:
```bash
pytest tests/ --browser webkit --browser chromium -v
```

## Test Coverage
| Area | Tests | Description |
|---|---|---|
| Homepage | 5 | Load, title, nav visibility |
| Navigation | 3 | Mac, iPhone, iPad routing |
| Search | 6 | Happy path, empty input, special characters, edge cases |
| Product Page | 6 | Heading, price, buy button, click flow |
| **Total** | **20** | WebKit + Chromium |

## Findings

### Finding 1 — HTTP 400 on Search Queries Containing `%`
**Test:** `test_search_special_characters`  
**Input:** `!@#$%`  
**Result:** HTTP 400 "Ambiguous URI path encoding" on both WebKit and Chromium  
**Root cause:** `%` is a URL reserved character for percent-encoding. Including 
it in a search query creates encoding ambiguity that Apple's server rejects.  
**Contrast:** `@#$` (without `%`) returns graceful "no matches" page ✅  
**Severity:** Low-Medium  
**Fix:** Sanitize/escape `%` before constructing the search URL  
**Filed:** Apple Feedback (apple.com/feedback) — May 2026  

## Bug Reports Filed
| ID | Summary | Filed To | Date | Status |
|---|---|---|---|---|
| BR-001 | HTTP 400 for `%` in search query | Apple Feedback | May 2026 | Submitted |