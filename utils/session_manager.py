from pages.login_page import LoginPage


class SessionManager:

    @staticmethod
    def login(page, username, password):
        login_page = LoginPage(page)

        login_page.login(username, password)
        login_page.wait_for_login_success()

        return login_page
