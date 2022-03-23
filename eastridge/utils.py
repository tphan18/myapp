"""Utils module. """

from flask import request
from jsonschema import validate, ValidationError
from werkzeug.exceptions import BadRequest


def get_payloads(schema=None):
    """Get the payloads from the request.

    Raises:
        BadRequest: If the payload is not valid JSON based on the schema.

    Returns:
        list: The list of payloads.
    """
    # Check if the mimetype is correct
    if not request.is_json:
        exception = BadRequest(
            "Invalid Content-Type header, should be application/json"
        )
        exception.code = 415
        raise exception

    # Validate if the payload is valid JSON
    try:
        payloads = request.get_json()
    except BadRequest as exception:
        exception.description = "Invalid JSON payload"
        raise exception

    # Valid the payloads based on the schema
    try:
        validate(instance=payloads, schema=schema)
    except ValidationError:
        raise BadRequest("Invalid JSON payload")

    return payloads
