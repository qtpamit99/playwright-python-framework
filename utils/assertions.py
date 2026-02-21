class Assert:

    @staticmethod
    def equals(actual, expected, message=""):
        assert actual == expected, \
            f" ASSERT EQUALS FAILED\nExpected: {expected}\nActual: {actual}\n{message}"

    @staticmethod
    def contains(item, collection, message=""):
        assert item in collection, \
            f" ASSERT CONTAINS FAILED\nItem: {item}\nCollection: {collection}\n{message}"

    @staticmethod
    def not_empty(collection, message=""):
        assert len(collection) > 0, \
            f" ASSERT NOT EMPTY FAILED\nCollection is empty\n{message}"

    @staticmethod
    def greater_than(value, threshold, message=""):
        assert value > threshold, \
            f" ASSERT GREATER THAN FAILED\nValue: {value}\nThreshold: {threshold}\n{message}"
