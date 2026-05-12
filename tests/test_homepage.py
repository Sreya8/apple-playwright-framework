from pages.homepage import HomePage
from playwright.sync_api import expect, Page
import pytest


def test_homepage_loads(page: Page):
    home = HomePage(page)
    home.navigate()

    home.should_be_on_homepage()
    page.screenshot(path="screenshots/homepage.png")


def test_nav_is_visible(page: Page):
    home = HomePage(page)
    home.navigate()

    home.nav_should_be_visible()

def test_mac_navigation(page: Page):
    home = HomePage(page)
    home.navigate()
    home.click_mac()

    expect(page).to_have_title("Mac - Apple")
    page.screenshot(path="screenshots/mac_page.png")

def test_iphone_navigation(page: Page):
    home = HomePage(page)
    home.navigate()
    home.click_iphone()

    expect(page).to_have_title("iPhone - Apple")
    page.screenshot(path="screenshots/iphone_page.png")

def test_ipad_navigation(page: Page):
    home = HomePage(page)
    home.navigate()
    home.click_ipad()

    expect(page).to_have_title("iPad - Apple")

