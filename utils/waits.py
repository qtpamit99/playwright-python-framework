from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class Wait:

    DEFAULT_TIMEOUT = 10000

    @staticmethod
    def for_visible(page, locator, timeout=DEFAULT_TIMEOUT):
        try:
            page.locator(locator).first.wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            raise AssertionError(f" WAIT FAILED → Element not visible: {locator}")

    @staticmethod
    def for_hidden(page, locator, timeout=DEFAULT_TIMEOUT):
        try:
            page.locator(locator).first.wait_for(state="hidden", timeout=timeout)
        except PlaywrightTimeoutError:
            raise AssertionError(f" WAIT FAILED → Element not hidden: {locator}")

    @staticmethod
    def for_text(page, locator, timeout=DEFAULT_TIMEOUT):
        try:
            page.locator(locator).first.wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            raise AssertionError(f" WAIT FAILED → Text not visible: {locator}")

    @staticmethod
    def for_count(page, locator, count, timeout=DEFAULT_TIMEOUT):
        try:
            page.wait_for_function(
                f"document.querySelectorAll('{locator}').length === {count}",
                timeout=timeout
            )
        except PlaywrightTimeoutError:
            raise AssertionError(
                f" WAIT FAILED → Expected {count} elements for: {locator}"
            )
