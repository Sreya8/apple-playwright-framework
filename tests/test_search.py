from pages.homepage import HomePage
from pages.searchpage import SearchPage
from playwright.sync_api import Page, expect
import re


def test_page_objects(page):
    # home and search will point to the same page. 
    # page is a reference and not a copy
    home = HomePage(page)
    home.navigate()                    # goes to apple.com

    search = SearchPage(page)
    search.search_for("MacBook")       # searches on the SAME tab

    assert home.page.url == search.page.url         # same URL — same tab


def test_search_opens(page):
    """Search input appears when search button is clicked"""
    home = HomePage(page)
    home.navigate()

    search = SearchPage(page)
    search.search_button.click()

    search.search_input_should_be_visible()
    page.screenshot(path="screenshots/search_open.png")


def test_search_macbook(page):
    """Searching MacBook navigates to results page"""
    home = HomePage(page)
    home.navigate()

    search = SearchPage(page)
    search.search_for("MacBook")
    
    search.url_should_contain_query("MacBook")
    # print("ACTUAL URL:", page.url())
    page.screenshot(path="screenshots/search_macbook.png")

def test_search_iPhone(page):
    """Searching iPhone navigates to results page"""
    home = HomePage(page)
    home.navigate()

    search = SearchPage(page)
    search.search_for("iPhone")

    search.url_should_contain_query("iPhone")
    # print("ACTUAL URL:", page.url())
    page.screenshot(path="screenshots/search_iPhone.png")

def test_search_empty(page):
    """Edge case — empty search should not crash"""
    home = HomePage(page)
    home.navigate()

    search = SearchPage(page)
    # search.search_for("")
    search.search_button.click()
    search.search_input.press("Enter")

    expect(page).to_have_url("https://www.apple.com/")
    page.screenshot(path="screenshots/search_empty.png")

def test_search_special_characters(page):
    """Edge case — special characters should not crash"""
    """
    Edge case — special characters in search.
    Finding: Both WebKit and Chromium return HTTP 400 
    'Ambiguous URI path encoding' for !@#$% input.
    Apple's server rejects the encoded URI.
    """
    home = HomePage(page)
    home.navigate()

    search = SearchPage(page)
    search.search_for("!@#$%")

    current_url = page.url
    page_content = page.content()
    print(f"URL: {current_url}")

    # Document the known behavior — server returns 400 for these characters
    # Apple.com does not handle !@#$% gracefully
    assert "apple.com" in current_url

    # Check if page shows error — document as known issue
    if "400" in page_content or "Ambiguous" in page_content:
        print("FINDING: HTTP 400 returned for special character search")
        print("Both WebKit and Chromium affected")
        # Don't fail the test — document the behavior instead
    
    page.screenshot(path="screenshots/search_special_chars.png")

def test_search_special_chars_without_percent(page):
    """
    Special characters WITHOUT % handle gracefully.
    Shows 'no matches found' page instead of HTTP 400.
    Contrast with test_search_special_characters which uses % and gets HTTP 400.
    """
    home = HomePage(page)
    home.navigate()

    search = SearchPage(page)
    search.search_for("@#$")

    print(f"URL: {page.url}")

    # Page should load on apple.com
    assert "apple.com" in page.url

    # Should show graceful no-results page — not a server error
    expect(page.locator("body")).not_to_contain_text("HTTP ERROR")
    expect(page.locator("body")).not_to_contain_text("Ambiguous URI")

    
    # Should show the friendly no-results message
    expect(page.locator(".rf-serp-nullsearch-title").first).to_be_visible()
    # expect(page.get_by_text("Sorry, no matches were found.")).to_be_visible()

    page.screenshot(path="screenshots/search_special_chars_no_percent.png")






