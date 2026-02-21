class LoginPage:
    def __init__(self, page):
        self.page = page

    def login(self, username, password):
        self.page.locator("#login2").click()
        self.page.locator("#logInModal").wait_for(state="visible")
        self.page.locator("#loginusername").fill(username)
        self.page.locator("#loginpassword").fill(password)
        self.page.locator("button:has-text('Log in')").click()

    def wait_for_login_success(self, timeout=10000):
        self.page.locator("#logout2").wait_for(state="visible", timeout=timeout)

    def get_logged_user(self):
        return self.page.locator("#nameofuser").inner_text()

    def is_logout_visible(self):
        return self.page.locator("#logout2").is_visible()

    def is_login_link_visible(self):
        return self.page.locator("#login2").is_visible()

    def is_signup_link_visible(self):
        return self.page.locator("#signin2").is_visible()