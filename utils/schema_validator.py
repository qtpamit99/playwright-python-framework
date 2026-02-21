class SchemaValidator:

    @staticmethod
    def validate_list(data, entity_name="Response"):
        if not isinstance(data, list):
            raise AssertionError(f" {entity_name} response is not a list")

    @staticmethod
    def validate_object(obj, schema, entity_name="Object"):

        if not isinstance(obj, dict):
            raise AssertionError(f" {entity_name} is not a dictionary")

        for field, expected_type in schema.items():

            if field not in obj:
                raise AssertionError(f" Missing field '{field}' in {entity_name}")

            if not isinstance(obj[field], expected_type):
                raise AssertionError(
                    f" Field '{field}' type mismatch in {entity_name}. "
                    f"Expected {expected_type}, got {type(obj[field])}"
                )

        return True

    @staticmethod
    def validate(data, schema, entity_name="Response"):
        """Smart validator for object"""

        if isinstance(data, dict):
            return SchemaValidator.validate_object(data, schema, entity_name)

        raise AssertionError(f" {entity_name} is not a valid object")