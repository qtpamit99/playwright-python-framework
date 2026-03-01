import allure
import pytest
import json

from utils.config_manager import get_credentials
from api_clients.auth_helper import AuthAPI
from utils.session_manager import SessionManager
from utils.token_manager import TokenManager


@allure.title("Login via UI → Validate Token via API")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.contract
def test_login_ui_api_contract(page, request):

    env_name = request.config.getoption("--env")

    # Credentials abstraction
    username, password = get_credentials(env_name)

    # ============================================
    # STEP 1 – UI Login (Reusable)
    # ============================================
    with allure.step(" Login via UI"):

        login_page = SessionManager.login(page, username, password)

        # UI VALIDATIONS
        assert login_page.is_logout_visible(), "Logout button not visible"
        assert not login_page.is_login_link_visible(), "Login link still visible"
        assert not login_page.is_signup_link_visible(), "Signup link still visible"

        displayed_user = login_page.get_logged_user()
        expected_user_text = f"Welcome {username}"

        assert displayed_user == expected_user_text, \
            f"Expected '{expected_user_text}', got '{displayed_user}'"

        screenshot_path = "ui_login_success.png"
        page.screenshot(path=screenshot_path)

        allure.attach.file(
            screenshot_path,
            name="UI after login",
            attachment_type=allure.attachment_type.PNG
        )

        print(f"UI Login successful – {displayed_user}")
        allure.attach(displayed_user, "UI Login Result")

    # ============================================
    # STEP 2 – Token Extraction (Utility Based )
    # ============================================
    with allure.step("🔍 Extract authentication token"):

        token, token_source = TokenManager.find_token(page)

        assert token, "No token found in browser"

        print(f"Token found in {token_source}: {token[:20]}...")

        allure.attach(
            f"Source: {token_source}\nToken: {token}",
            "Token Details"
        )

    # ============================================
    # STEP 3 – API Token Validation
    # ============================================
    with allure.step("Validate token via /check API"):

        auth_api = AuthAPI(page.request, env_name)

        response = auth_api.check_token(token)

        assert "Item" in response, f"Missing 'Item' in response: {response}"

        item = response["Item"]

        # TOKEN VALIDATION
        assert "token" in item, "Token missing in API response"
        assert item["token"] == token, \
            f"Token mismatch → Sent: {token} | Got: {item['token']}"

        print(f"Token validated: {item['token'][:20]}...")

        #  USERNAME VALIDATION
        assert "username" in item, " Username missing"
        assert item["username"] == username, \
            f"Username mismatch → UI: {username} | API: {item['username']}"

        print(f" Username validated: {item['username']}")

        # EXPIRATION VALIDATION
        assert "expiration" in item, "Expiration missing"

        print(f"Token expiration: {item['expiration']}")

        allure.attach(
            json.dumps(response, indent=2),
            "API Response",
            allure.attachment_type.JSON
        )

    # ============================================
    # FINAL STEP
    # ============================================
    with allure.step("Contract Validation Complete"):

        summary = (
            f"UI User: {displayed_user}\n"
            f"API User: {item['username']}\n"
            f"Token Source: {token_source}\n"
            f"Token Valid: Yes\n"
            f"Expiration: {item['expiration']}"
        )

        allure.attach(summary, "Validation Summary")

        print("\n UI & API Contract VALID ")
