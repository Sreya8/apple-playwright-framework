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

### Finding 1 — HTTP 400 on Any Search Query Containing `%`
**Test:** `test_search_special_characters`, `test_search_percent_in_normal_query`  
**Affected inputs:** Any query containing `%` (e.g. `!@#$%`, `Mac % Book`)  
**Result:** HTTP 400 "Ambiguous URI path encoding" on both WebKit and Chromium  
**Root cause:** `%` is a reserved URL character for percent-encoding. Any query  
containing `%` creates encoding ambiguity that Apple's server rejects.  
**Contrast:**  
- `@#$` (without `%`) → graceful "no matches" page ✅  
- `MacBook` → works correctly ✅  
- `Mac % Book` → HTTP 400 ❌  
- `!@#$%` → HTTP 400 ❌  
**Affected browsers:** Both WebKit and Chromium  
**Severity:** Medium — affects any user searching with `%` in their query  
**Fix:** Sanitize/escape `%` before constructing the search URL  
**Filed:** Apple Feedback Assistant — Web & Services / WebKit — May 2026  

## Bug Reports Filed
| ID | Summary | Platform | Technology | Date | Status |
|---|---|---|---|---|---|
| FB22823503 | HTTP 400 for `%` in search query | Web & Services | WebKit | May 2026 | Submitted |


### Finding 2 — Critical Accessibility Violations on Apple.com

#### Homepage
| Severity | Rule | Description | Elements Affected |
|---|---|---|---|
| CRITICAL | aria-required-children | ARIA role missing required child roles | 2 |
| SERIOUS | color-contrast | Foreground/background contrast below WCAG AA | 1 |
| MODERATE | region | Page content not contained by landmarks | 1 |
| MINOR | aria-allowed-role | Invalid role attribute value | 2 |

#### MacBook Air Product Page
| Severity | Rule | Description | Elements Affected |
|---|---|---|---|
| CRITICAL | aria-required-children | ARIA role missing required child roles | 1 |
| CRITICAL | select-name | Select element has no accessible name | 1 |
| SERIOUS | color-contrast | Contrast below WCAG AA — 40 elements | 40 |
| MINOR | aria-allowed-role | Invalid role attribute value | 11 |

#### Search Results Page
No violations found ✅

**Most impactful finding:** The `select-name` violation on the MacBook Air 
product page means blind users using VoiceOver cannot identify the purpose 
of a dropdown in the purchase flow — directly impacting accessibility 
of Apple's own purchase experience.