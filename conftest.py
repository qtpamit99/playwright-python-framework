import shutil
import pytest
import time
import gc
import os
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from config import HEADLESS
from db.db_client import DBClient
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.place_order_page import PlaceOrderPage
import allure
import requests

from utils.debug_helper import DebugHelper
from utils.failure_analyzer import FailureAnalyzer
from api_clients.product_api import ProductAPI
from config.settings import settings


# ================= ROOT DETECTION =================
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


# ================= CLI OPTIONS =================
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev")
    parser.addoption("--ui-device", action="store", default="desktop")


# ================= ENV SYNC =================
def pytest_configure(config):
    env_name = config.getoption("--env")
    os.environ["TEST_ENV"] = env_name


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
def page(browser, request, playwright):

    if not settings.BASE_URL:
        raise ValueError(f"BASE_URL missing for env: {settings.ENV}")

    # ================= CART CLEANUP =================
    try:
        payload = {"cookie": settings.CREDENTIALS["username"]}
        requests.post(
            f"{settings.API_URL}/deletecart",
            json=payload,
            timeout=10
        )
    except Exception as e:
        print(f"[WARNING] Cart cleanup failed: {str(e)}")

    # ================= DEVICE HANDLING =================
    device_name = request.config.getoption("--ui-device")

    if device_name.lower() == "desktop":

        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(VIDEO_DIR),
            record_video_size={"width": 1280, "height": 720}
        )

        print("[INFO] Running in DESKTOP mode")

    else:
        try:
            device_config = playwright.devices[device_name]

            context = browser.new_context(
                **device_config,
                record_video_dir=str(VIDEO_DIR)
            )

            print(f"[INFO] Running on device: {device_name}")

        except KeyError:
            available = list(playwright.devices.keys())[:15]
            raise ValueError(
                f"Device '{device_name}' not found.\n"
                f"Example available devices: {available}"
            )

    page = context.new_page()

    page.__console_logs = []
    page.__network_failures = []

    page.on("console", lambda msg: page.__console_logs.append(f"{msg.type}: {msg.text}"))
    page.on("requestfailed", lambda req: page.__network_failures.append(req.url))

    try:
        page.goto(settings.BASE_URL, timeout=60000, wait_until="domcontentloaded")
        page.set_default_timeout(10000)
    except PlaywrightTimeoutError:
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        page.screenshot(path=str(SCREENSHOT_DIR / "NAV_TIMEOUT.png"))
        raise

    yield page

    # ================= FAILURE CHECK =================
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:
        DebugHelper.attach_page_state(page)

        SCREENSHOT_DIR.mkdir(exist_ok=True)
        screenshot_path = SCREENSHOT_DIR / f"FAIL_{request.node.name}.png"

        page.screenshot(path=str(screenshot_path))

        with open(screenshot_path, "rb") as f:
            allure.attach(
                f.read(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

    # Close context first
    context.close()
    time.sleep(0.5)

    # ================= VIDEO HANDLING =================
    if page.video:
        try:
            video_path = Path(page.video.path())

            if failed and video_path.exists():

                FAIL_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = request.node.name.replace("[", "_").replace("]", "_")

                new_video = FAIL_VIDEO_DIR / f"FAIL_{safe_name}_{timestamp}.webm"

                shutil.copy2(video_path, new_video)

                with open(new_video, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="Failure Video",
                        attachment_type=allure.attachment_type.WEBM
                    )

                video_path.unlink()

            elif not failed and video_path.exists():
                video_path.unlink()

        except Exception as e:
            print(f"[WARNING] Video cleanup error: {str(e)}")

    gc.collect()


# ================= API REQUEST FIXTURE =================
@pytest.fixture(scope="function")
def api_request(playwright):

    if not settings.API_URL:
        raise ValueError(f"API_URL missing for env: {settings.ENV}")

    ctx = playwright.request.new_context(base_url=settings.API_URL)
    yield ctx
    ctx.dispose()


# ================= PRODUCT API FIXTURE =================
@pytest.fixture(scope="function")
def product_api(api_request):
    return ProductAPI(
        request_context=api_request,
        env_config={"api_url": settings.API_URL}
    )


# ================= DB FIXTURE =================
@pytest.fixture(scope="function")
def db_client():
    client = DBClient()
    yield client
    client.close()


# ================= POM FIXTURE =================
@pytest.fixture
def pages(page):
    return {
        "home": HomePage(page),
        "cart": CartPage(page),
        "order": PlaceOrderPage(page)
    }


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
            name="Failure Classification",
            attachment_type=allure.attachment_type.TEXT
        )