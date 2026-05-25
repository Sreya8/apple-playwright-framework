from pages.homepage import HomePage
from pages.searchpage import SearchPage
from pages.product_page import ProductPage
from axe_playwright_python.sync_playwright import Axe


def run_axe_audit(page, screenshot_name: str) -> list:
    """
    Runs axe-core audit and returns violations.
    Waits for full page load before scanning — prevents flaky results.
    """
    # networkidle = safest option — waits until all assets, scripts, API calls done
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    axe = Axe()
    results = axe.run(page)
    page.screenshot(path=f"screenshots/{screenshot_name}.png", full_page=True)

    violations = results.response["violations"]

    if violations:
        print(f"\n{len(violations)} accessibility violation(s) found:")
        for v in violations:
            print(f"  [{v['impact'].upper()}] {v['id']}: {v['description']}")
            print(f"  Affected elements: {len(v['nodes'])}")
    else:
        print("\nNo accessibility violations found ✅")

    return violations


def print_severity_summary(violations: list, page_name: str) -> dict:
    """Prints severity breakdown and returns counts."""
    critical = [v for v in violations if v["impact"] == "critical"]
    serious  = [v for v in violations if v["impact"] == "serious"]
    moderate = [v for v in violations if v["impact"] == "moderate"]
    minor    = [v for v in violations if v["impact"] == "minor"]

    print(f"\n--- Accessibility Audit: {page_name} ---")
    print(f"Critical : {len(critical)}")
    print(f"Serious  : {len(serious)}")
    print(f"Moderate : {len(moderate)}")
    print(f"Minor    : {len(minor)}")
    print(f"Total    : {len(violations)}")

    return {
        "critical": critical,
        "serious": serious,
        "moderate": moderate,
        "minor": minor
    }


def test_homepage_accessibility(page):
    """Audit Apple.com homepage for WCAG violations — documents findings"""
    home = HomePage(page)
    home.navigate()

    violations = run_axe_audit(page, "a11y_homepage")
    print_severity_summary(violations, "Homepage")

    assert True


def test_search_results_accessibility(page):
    """Audit search results page for WCAG violations — documents findings"""
    home = HomePage(page)
    home.navigate()

    search = SearchPage(page)
    search.search_for("MacBook")

    violations = run_axe_audit(page, "a11y_search_results")
    print_severity_summary(violations, "Search Results")

    assert True


def test_product_page_accessibility(page):
    """Audit MacBook Air product page for WCAG violations — documents findings"""
    product = ProductPage(page)
    product.navigate()

    violations = run_axe_audit(page, "a11y_product_page")
    print_severity_summary(violations, "Product Page")

    assert True

def test_no_critical_violations_homepage(page):
    """
    Enforcement test — documents critical violations found on Apple homepage.
    Known violations filed to Apple Feedback Assistant.
    """
    home = HomePage(page)
    home.navigate()

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    axe = Axe()
    results = axe.run(page)
    violations = results.response["violations"]
    critical = [v for v in violations if v["impact"] == "critical"]

    if critical:
        print(f"\nKNOWN CRITICAL violations ({len(critical)}) — filed to Apple:")
        for v in critical:
            print(f"  {v['id']}: {v['description']}")
            for node in v["nodes"]:
                print(f"  Element: {node['html']}")

    # Document known violations — update this number if Apple fixes them
    # Currently known: 1 critical on homepage (aria-required-children)
    assert len(critical) <= 1, \
        f"New critical violation detected — previously only 1 known, now {len(critical)}"


def test_no_critical_violations_product_page(page):
    """
    Enforcement test — documents critical violations on MacBook Air page.
    Known violations filed to Apple Feedback Assistant.
    """
    product = ProductPage(page)
    product.navigate()

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    axe = Axe()
    results = axe.run(page)
    violations = results.response["violations"]
    critical = [v for v in violations if v["impact"] == "critical"]

    if critical:
        print(f"\nKNOWN CRITICAL violations ({len(critical)}) — filed to Apple:")
        for v in critical:
            print(f"  {v['id']}: {v['description']}")

    # Currently known: 2 critical on product page
    assert len(critical) <= 2, \
        f"New critical violation detected — previously 2 known, now {len(critical)}"