from playwright.sync_api import TimeoutError
import time
from contextlib import contextmanager


class Actions:

    @staticmethod
    def safe_click(locator, retries=3):

        for attempt in range(retries):

            try:
                locator.wait_for(state="visible", timeout=5000)
                locator.click()
                return

            except Exception as e:

                if attempt == retries - 1:
                    raise AssertionError(f" Click failed after {retries} attempts → {str(e)}")

                time.sleep(1.0)

    @staticmethod
    @contextmanager
    def accept_dialog(page):
        """Wait for dialog and auto-accept"""
        with page.expect_event("dialog") as dialog_info:
            yield

        dialog = dialog_info.value
        dialog.accept()

    @staticmethod
    def safe_fill(locator, value, retries=3):

        for attempt in range(retries):

            try:
                locator.wait_for(state="visible", timeout=5000)
                locator.fill(value)
                return

            except Exception as e:

                if attempt == retries - 1:
                    raise AssertionError(f" Fill failed after {retries} attempts → {str(e)}")

                time.sleep(1.0)
