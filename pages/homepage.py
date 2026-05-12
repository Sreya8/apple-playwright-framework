from playwright.sync_api import Page, expect

class HomePage:

    URL = "https://www.apple.com"

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.nav = page.locator("#globalnav")
        self.mac_link = self.nav.get_by_role("link", name="Mac")
        self.iphone_link = self.nav.get_by_role("link", name="iPhone")
        self.ipad_link = self.nav.get_by_role("link", name="iPad")
        self.search_button = self.nav.get_by_role("button", name="Search apple.com")

    
    # Actions

    def navigate(self):
        self.page.goto(self.URL)

    def click_mac(self):
        self.mac_link.click()
    
    def click_iphone(self):
        self.iphone_link.click()
    
    def click_ipad(self):

        self.ipad_link.click()
    
    def click_search(self):
        self.search_button.click()
    

    # Getters

    def get_title(self):
        return self.page.title()

    def get_url(self):
        return self.page.url()


    # Assertions

    def should_be_on_homepage(self):
        expect(self.page).to_have_title("Apple")
    
    def nav_should_be_visible(self):
        expect(self.nav).to_be_visible()