INVOICE_ITEMS_SCHEMA = {
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "object",
        "required": ["units", "description", "amount"],
        "properties": {
            "units": {
                "type": "integer",
                "minimum": 1,
            },
            "description": {
                "type": "string",
                "minLength": 1,
            },
            "amount": {
                "type": "number",
                "minimum": 0,
            },
        },
    },
}
