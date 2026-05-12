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
    home = HomePage(page)
    home.navigate()

    search = SearchPage(page)
    search.search_for("!@#$%")

    search.get_current_url()

    assert "apple.com" in page.url
    page.screenshot(path="screenshots/search_special_chars.png")






