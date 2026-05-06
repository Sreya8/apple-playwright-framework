from pages.homepage import HomePage
from playwright.sync_api import expect
import time


def test_apple_homepage_title(page):
    home_page = HomePage(page)

    home_page.navigate()

    assert "Apple" in home_page.get_title()

    page.screenshot(path="screenshots/homepage.png")
    # time.sleep(5)


def test_mac_navigation(page):
    home_page = HomePage(page)
    home_page.navigate()
    home_page.click_mac()

    expect(page).to_have_title("Mac - Apple")

    page.screenshot(path="screenshots/mac_page.png")


