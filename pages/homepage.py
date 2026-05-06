class HomePage:
    def __init__(self, page):
        self.page = page
    
    def navigate(self):
        self.page.goto("https://www.apple.com")
    
    def get_title(self):
        return self.page.title()

    def click_mac(self):
        # self.page.get_by_role("link", name="Mac").click()
        self.page.locator("#globalnav").get_by_role("link", name="Mac").click()