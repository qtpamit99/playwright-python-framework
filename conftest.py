import shutil
import pytest
import time
import gc
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from config import HEADLESS
from db.db_client import DBClient
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.place_order_page import PlaceOrderPage
from utils.config_manager import load_environment_config
import allure
from utils.debug_helper import DebugHelper
from utils.failure_analyzer import FailureAnalyzer
from api_clients.product_api import ProductAPI



# ================= ROOT DETECTION (BULLETPROOF) =================
def get_project_root():
    current = Path(__file__).resolve()

    while current != current.parent:

        if (current / "requirements.txt").exists() \
           or (current / "pyproject.toml").exists() \
           or (current / ".git").exists():
            return current

        current = current.parent

    raise RuntimeError("Project root not found")


PROJECT_ROOT = get_project_root()

SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"
VIDEO_DIR = PROJECT_ROOT / "videos"
FAIL_VIDEO_DIR = VIDEO_DIR / "failures"


# ================= PLAYWRIGHT =================
@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


# ================= BROWSER =================
@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=HEADLESS)
    yield browser
    browser.close()
    time.sleep(1.0)


# ================= PAGE FIXTURE =================
@pytest.fixture(scope="function")
def page(browser, request):

    env_name = request.config.getoption("--env")
    env_config = load_environment_config(env_name)

    base_url = env_config.get("base_url")
    if not base_url:
        raise ValueError(f"base_url missing for env: {env_name}")

    context = browser.new_context(
        record_video_dir=str(VIDEO_DIR),
        record_video_size={"width": 1280, "height": 720}
    )

    page = context.new_page()

    # ── Runtime Telemetry ──
    page.__console_logs = []
    page.__network_failures = []

    page.on("console", lambda msg: page.__console_logs.append(f"{msg.type}: {msg.text}"))
    page.on("requestfailed", lambda req: page.__network_failures.append(req.url))

    # ── Navigation ──
    try:
        page.goto(base_url, timeout=60000, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        page.screenshot(path="error_nav_timeout.png")
        raise

    yield page

    # ── Detect failure ──
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:

        DebugHelper.attach_page_state(page)

        # ================= SCREENSHOT =================
        SCREENSHOT_DIR.mkdir(exist_ok=True)

        screenshot_path = SCREENSHOT_DIR / f"FAIL_{request.node.name}.png"

        page.screenshot(path=str(screenshot_path))

        print(f"→ Screenshot saved: {screenshot_path}")

        with open(screenshot_path, "rb") as f:
            allure.attach(
                f.read(),
                name="📸 Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

    # ⭐ CLOSE CONTEXT FIRST ⭐
    context.close()
    time.sleep(0.6)

    # ================= VIDEO HANDLING =================
    if page.video:
        try:
            video_path = Path(page.video.path())

            if failed and video_path.exists():

                FAIL_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                safe_test_name = request.node.name.replace("[", "_").replace("]", "_").replace("::", "_")

                new_video_path = FAIL_VIDEO_DIR / f"FAIL_{safe_test_name}_{timestamp}.webm"

                shutil.copy2(video_path, new_video_path)

                print(f"→ Failure video saved → {new_video_path}")

                with open(new_video_path, "rb") as video_file:
                    allure.attach(
                        video_file.read(),
                        name="🎥 Failure Video",
                        attachment_type=allure.attachment_type.WEBM
                    )

                video_path.unlink()
                print("→ Deleted original random video")

            elif not failed and video_path.exists():

                video_path.unlink()
                print(f"[INFO] Deleted PASS video: {video_path}")

        except Exception as e:
            print(f"[WARNING] Video cleanup error: {str(e)}")

    gc.collect()


# ================= API REQUEST FIXTURE =================
@pytest.fixture(scope="function")
def api_request(playwright, request):

    env_name = request.config.getoption("--env")
    env_config = load_environment_config(env_name)

    api_url = env_config.get("api_url")
    if not api_url:
        raise ValueError(f"api_url missing for env: {env_name}")

    ctx = playwright.request.new_context(base_url=api_url)
    yield ctx
    ctx.dispose()


# ================= PRODUCT API FIXTURE =================
@pytest.fixture(scope="function")
def product_api(api_request, request):

    env_name = request.config.getoption("--env")
    env_config = load_environment_config(env_name)

    return ProductAPI(
        request_context=api_request,
        env_config=env_config
    )


# ================= DB FIXTURE =================
@pytest.fixture(scope="function")
def db_client():
    client = DBClient()
    yield client
    client.close()


# ================= POM PAGES FIXTURE =================
@pytest.fixture
def pages(page):
    return {
        "home": HomePage(page),
        "cart": CartPage(page),
        "order": PlaceOrderPage(page)
    }


# ================= CLI OPTION =================
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev")


# ================= REPORT HOOK =================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    item.rep_call = report

    if report.failed:
        failure_type = FailureAnalyzer.classify(str(report.longrepr))

        allure.attach(
            failure_type,
            name=" Failure Classification",
            attachment_type=allure.attachment_type.TEXT
        )