import json


class TokenManager:

    @staticmethod
    def find_token(page):

        local_storage = page.evaluate("""() => {
            const items = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                items[key] = localStorage.getItem(key);
            }
            return items;
        }""")

        session_storage = page.evaluate("""() => {
            const items = {};
            for (let i = 0; i < sessionStorage.length; i++) {
                const key = sessionStorage.key(i);
                items[key] = sessionStorage.getItem(key);
            }
            return items;
        }""")

        cookies = page.context.cookies()

        token = None
        token_source = None

        for key in ["token", "access_token", "auth_token", "session_token", "Token"]:
            if key in local_storage and local_storage[key]:
                return local_storage[key], f"localStorage['{key}']"

        for key in ["token", "access_token", "auth_token", "session_token", "Token"]:
            if key in session_storage and session_storage[key]:
                return session_storage[key], f"sessionStorage['{key}']"

        for cookie in cookies:
            if "token" in cookie["name"].lower():
                return cookie["value"], f"cookie '{cookie['name']}'"

        return None, None
