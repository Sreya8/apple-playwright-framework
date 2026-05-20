from playwright.sync_api import Page, expect

class ProductPage:

    URL = "https://www.apple.com/macbook-air/"

    def __init__(self, page: Page):
        self.page = page
        
        # Scope to hero section — all three elements live inside here
        self.hero = page.locator("section.section-hero .section-content")

        # Locators scoped to hero — no ambiguity
        self.product_heading = self.hero.locator(".header-eyebrow")
        self.product_price = self.hero.locator("[data-pricing-product='macbook-air-main']").first
        self.buy_link = self.hero.get_by_role("link", name="Buy, MacBook Air")
    
    # --- Actions ---
    def navigate(self) -> None:
        self.page.goto(self.URL)
    
    def click_buy(self) -> None:
        self.buy_link.click()


    # --- Getters ---
    def get_title(self) -> str:
        return self.page.title()

    def get_price(self) -> str:
        return self.product_price.inner_text()
    
    
    # --- Assertions ---
    def should_show_heading(self) -> None:
        expect(self.product_heading).to_be_visible()

    def should_show_price(self) -> None:
        expect(self.product_price).to_be_visible()

    def should_show_buy_button(self) -> None:
        expect(self.buy_link).to_be_visible()
