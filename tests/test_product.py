from pages.product_page import ProductPage
from playwright.sync_api import expect
import re

def test_product_page_loads(page):
    product = ProductPage(page)
    product.navigate()
    expect(page).to_have_title("MacBook Air 13-inch and MacBook Air 15-inch - Apple")

def test_product_heading_visible(page):
    product = ProductPage(page)
    product.navigate()
    product.should_show_heading()

def test_product_price_visible(page):
    product = ProductPage(page)
    product.navigate()
    product.should_show_price()

def test_buy_button_visible(page):
    product = ProductPage(page)
    product.navigate()
    product.should_show_buy_button()

def test_buy_button_click(page):
    product = ProductPage(page)
    product.navigate()
    product.click_buy()

    # expect(page).to_have_title("Buy MacBook Air - Apple")
    expect(page).to_have_url(re.compile(r"apple\.com/.*shop.*macbook-air"))

def test_price_is_not_empty(page):
    product = ProductPage(page)
    product.navigate()
    price = product.get_price()
    # Expect only works on playwright objects
    # assert price != ""
    # Can use expect on product.product_price since it is a locator. Not on get_price()
    expect(product.product_price).not_to_be_empty()