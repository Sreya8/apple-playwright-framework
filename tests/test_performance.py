import time
from pages.homepage import HomePage
from pages.searchpage import SearchPage
from pages.product_page import ProductPage
from playwright.sync_api import expect
import OS

# CI servers are slower than local — use higher threshold in CI
IS_CI = os.environ.get("CI") == "true"

# Performance thresholds - Apple's own web performance standards
HOMEPAGE_MAX_LOAD = 10 if IS_CI else 5.0 #seconds
SEARCH_MAX_RESPONSE = 10 if IS_CI else 5.0
PRODUCT_MAX_LOAD = 10 if IS_CI else 5.0
NAV_MAX_TRANSITION = 10 if IS_CI else 5.0


def measure_load_time(page, url: str) -> float:
    """
    Navigates to URL and returns load time in seconds.
    Uses networkidle — waits for all assets to finish loading.
    """
    start = time.time()
    page.goto(url, wait_until="networkidle")
    end = time.time()

    load_time = round(end - start, 2)
    print(f"\nLoad time for {url}: {load_time}s")
    return load_time

def test_homepage_load_time(page):
    """Homepage should load within threshold"""
    load_time = measure_load_time(page, "https://www.apple.com")
    
    print(f"\nHomepage load time: {load_time}s (threshold: {HOMEPAGE_MAX_LOAD}s)")
    assert load_time < HOMEPAGE_MAX_LOAD, f"HomePage too slow: {load_time}s exceeds {HOMEPAGE_MAX_LOAD}s threshold"

def test_product_page_load_time(page):
    """MacBook Air product page should load within threshold"""
    load_time = measure_load_time(page, "https://www.apple.com/macbook-air/")

    print(f"\nProduct page load time: {load_time}s (threshold: {PRODUCT_MAX_LOAD}s)")
    assert load_time < PRODUCT_MAX_LOAD, f"Product page too slow: {load_time}s exceeds {PRODUCT_MAX_LOAD}s threshold"

def test_search_response_time(page):
    """Search results should appear within threshold"""
    home = HomePage(page)
    home.navigate()

    start = time.time()
    search = SearchPage(page)
    search.search_for("MacBook")
    page.wait_for_load_state("networkidle")
    end = time.time()

    response_time = round(end - start, 2)

    print(f"Search response time: {response_time}s (threshold: {SEARCH_MAX_RESPONSE}s)")

    assert response_time < SEARCH_MAX_RESPONSE, \
        f"Search too slow: {response_time}s exceeds {SEARCH_MAX_RESPONSE}s threshold"

def test_nav_transition_time(page):
    """Nav click to page load should be within threshold"""
    home = HomePage(page)
    home.navigate()

    start = time.time()
    home.click_mac()
    page.wait_for_load_state("networkidle")
    end = time.time()

    transition_time = round(end - start, 2)

    print(f"Nav transition time: {transition_time}s (threshold: {NAV_MAX_TRANSITION}s)")

    assert transition_time < NAV_MAX_TRANSITION, \
        f"Nav transition too slow: {transition_time}s exceeds {NAV_MAX_TRANSITION}s threshold"
