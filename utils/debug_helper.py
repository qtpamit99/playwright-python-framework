import allure


class DebugHelper:

    @staticmethod
    def attach_page_state(page):

        # URL
        try:
            allure.attach(page.url, " Page URL", allure.attachment_type.TEXT)
        except:
            pass

        # DOM
        try:
            allure.attach(page.content(), "DOM Snapshot", allure.attachment_type.HTML)
        except:
            pass

        # Console
        try:
            if page.__console_errors:
                allure.attach(
                    "\n".join(page.__console_errors),
                    " Console Logs",
                    allure.attachment_type.TEXT
                )
        except:
            pass

        # Network
        try:
            if page.__network_failures:
                allure.attach(
                    "\n".join(page.__network_failures),
                    " Network Failures",
                    allure.attachment_type.TEXT
                )
        except:
            pass
