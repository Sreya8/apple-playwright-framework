# Apple.com Automation Framework

A production-style test automation framework targeting live Apple.com, 
built with Python, Playwright, and WebKit - Apple's open source Safari engine.

## Tech Stack
- **Python 3.10**
- **Playwright** - browser automation with WebKit and Chromium
- **pytest** - test runner and fixture management
- **axe-core** - automated WCAG accessibility auditing
- **WebKit** - Apple's open source Safari engine (same engine powering Safari, 
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
├── test_product.py
└── test_accessibility.py
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
| Homepage | 5 | Load, title, nav visibility, navigation bar |
| Navigation | 3 | Mac, iPhone, iPad routing |
| Search | 8 | Happy path, empty input, special characters, % edge cases |
| Product Page | 6 | Heading, price, buy button, click flow |
| Accessibility | 5 | axe-core WCAG audit — homepage, search, product page; critical violation enforcement |
| **Total** | **24** | WebKit (default) + Chromium (cross-browser) |

## Bug Reports Filed
| ID | Summary | Platform | Technology | Date | Status |
|---|---|---|---|---|---|
| FB22823503 | HTTP 400 for `%` in search query | Web & Services | WebKit | May 2026 | Submitted |
| FB22851540 | MacBook Air dropdown has no accessible name — VoiceOver cannot identify purpose | Web & Services | WebKit / Accessibility | May 2026 | Submitted |

## Findings

### Finding 1 — HTTP 400 on Any Search Query Containing `%`
**Tests:** `test_search_special_characters`, `test_search_percent_in_normal_query`  
**Affected inputs:** Any query containing `%` (e.g. `!@#$%`, `Mac % Book`)  
**Result:** HTTP 400 "Ambiguous URI path encoding" on both WebKit and Chromium  
**Root cause:** `%` is a reserved URL character for percent-encoding. Any query containing `%` creates encoding ambiguity that Apple's server rejects.  
**Contrast:**
- `@#$` (without `%`) → graceful "no matches" page ✅
- `MacBook` → works correctly ✅
- `Mac % Book` → HTTP 400 ❌
- `!@#$%` → HTTP 400 ❌

**Affected browsers:** Both WebKit and Chromium  
**Severity:** Medium — affects any user searching with `%` in their query  
**Fix:** Sanitize/escape `%` before constructing the search URL  
**Filed:** Apple Feedback Assistant — FB22823503 — May 2026

---

### Finding 2 — Critical Accessibility Violations on Apple.com (WCAG Audit)

Automated axe-core accessibility audit identified WCAG violations across Apple.com pages.

#### Homepage — 4 violations
| Severity | Rule | Description | Elements Affected |
|---|---|---|---|
| CRITICAL | `aria-required-children` | ARIA `role="list"` missing required child roles — breaks screen reader navigation of media gallery | 2 |
| SERIOUS | `color-contrast` | Foreground/background contrast below WCAG 2 AA minimum | 1 |
| MODERATE | `region` | Page content not contained within landmark regions | 1 |
| MINOR | `aria-allowed-role` | Invalid role attribute value on element | 2 |

#### MacBook Air Product Page — 4 violations
| Severity | Rule | Description | Elements Affected |
|---|---|---|---|
| CRITICAL | `select-name` | "Select your current MacBook Air" dropdown has no accessible name — VoiceOver users cannot identify its purpose in the purchase flow | 1 |
| CRITICAL | `aria-required-children` | ARIA `role="list"` missing required child roles in product gallery | 1 |
| SERIOUS | `color-contrast` | Contrast below WCAG 2 AA — affects 40 elements | 40 |
| MINOR | `aria-allowed-role` | Invalid role attribute value | 11 |

#### Search Results Page
No violations found ✅

#### Most impactful finding — `select-name` on MacBook Air page
The "Select your current MacBook Air" dropdown in the upgrade comparison section 
has no programmatic label. The visible label is a `<span>` with no connection 
to the `<select>` element.

A blind VoiceOver user hears:
- **Current:** `"MacBook Air (M1), select element"`
- **Should hear:** `"Select your current MacBook Air, MacBook Air (M1), select element"`

This directly impacts a blind user's ability to compare models before making 
a purchase decision.

**Root cause:** Label is a `<span>`, not a `<label for="upgraders-select">`  
**WCAG violation:** 1.3.1 Info and Relationships (Level A)  
**Fix:** Change `<span>` to `<label for="upgraders-select">` or add `aria-label` to the `<select>`  
**Filed:** Apple Feedback Assistant — FB22851540 — May 2026