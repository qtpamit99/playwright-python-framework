class SoftAssert:

    def __init__(self):
        self.errors = []

    def equals(self, actual, expected, message=""):
        if actual != expected:
            self.errors.append(
                f"SOFT ASSERT FAILED → {message}\nExpected: {expected}\nActual: {actual}\n"
            )

    def contains(self, item, collection, message=""):
        if item not in collection:
            self.errors.append(
                f"SOFT ASSERT FAILED → {message}\nItem: {item}\nCollection: {collection}\n"
            )

    def not_empty(self, value, message=""):
        if not value:
            self.errors.append(
                f"SOFT ASSERT FAILED → {message}\nValue: {value}\n"
            )

    def assert_all(self):
        if self.errors:
            combined = "\n\n".join(self.errors)
            raise AssertionError(combined)