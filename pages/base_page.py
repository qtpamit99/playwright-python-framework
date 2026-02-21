class BasePage:

    def __init__(self, page):
        self.page = page

    def get_title(self):
        return self.page.title()

    def click(self, locator):
        self.page.click(locator)

    def fill(self, locator, value):
        self.page.fill(locator, value)
