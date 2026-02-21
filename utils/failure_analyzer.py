class FailureAnalyzer:

    @staticmethod
    def classify(error_message):

        error_message = error_message.lower()

        if "timeout" in error_message:
            return "⏱ TIMEOUT / SYNC ISSUE"

        if "locator" in error_message:
            return " LOCATOR / UI CHANGE"

        if "network" in error_message:
            return " NETWORK FAILURE"

        if "api" in error_message:
            return " API FAILURE"

        if "assert" in error_message:
            return " ASSERTION / DATA FAILURE"

        return " UNKNOWN FAILURE"
