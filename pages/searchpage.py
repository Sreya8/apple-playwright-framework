from playwright.sync_api import Page, expect
import re

class SearchPage:

    def __init__(self, page: Page):
        self.page = page
    

        # Locators found via codegen
        self.search_input = page.get_by_role("textbox", name="Search apple.com")
        self.search_button = page.get_by_role("button", name="Search apple.com")

        # Results container
        self.results_container = page.locator("#results")
    
    # --- Actions ---

    def search_for(self, query: str) -> None:
        # Full search flow: Click -> Type -> Submit

        self.search_button.click()
        self.search_input.fill(query)
        self.search_input.press("Enter")
    
    def clear_and_search(self, query: str) -> None:
        # Clear the existing search and type a new one

        self.search_button.click()
        self.search_input.fill(query)
        self.search_input.press("Enter")
    
    # --- Getters ---
    def get_search_value(self) -> str:
        # Returns whatever is currently typed in the search box
        return self.search_input.input_value()

    def get_current_url(self) -> str:
        return self.page.url

    # --- Assertions ---
    def search_input_should_be_visible(self) -> None:
        expect(self.search_input).to_be_visible()
    
    def should_show_results(self) -> None:
        expect(self.results_container).to_be_visible()
    
    def url_should_contain_query(self, query: str) -> None:
        expect(self.page).to_have_url(re.compile(rf"apple\.com/.*search/{query}"))