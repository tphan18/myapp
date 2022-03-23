# Endpoints

```text
    POST    /v1/invoices          Create an invoice with its items
     GET    /v1/invoices          List all invoices
    POST    /v1/invoices/:id      Add items with the given ID
     GET    /v1/invoices/:id      Get invoice with the given ID
```

# POST /v1/invoices

**Required keys**

- units: integer
- description: string
- amount: number

**Example**

```bash
curl --request POST 'http://localhost:5000/v1/invoices' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "units": 2,
        "description": "foo",
        "amount": 1
    },
    {
        "units": 2,
        "description": "bar",
        "amount": 1.2
    }
]'
```

**Response**

```json
{
  "id": "256aae12-5c7f-4e2e-bfff-47cfcb7e4db5",
  "invoice_date": "Wed, 23 Mar 2022 00:25:17 GMT",
  "invoice_items": [
    {
      "amount": 1.0,
      "description": "foo",
      "id": "9cadaab0-e7b6-414c-bd8b-b613f52ff47c",
      "units": 2
    },
    {
      "amount": 1.2,
      "description": "bar",
      "id": "1c9e72f8-cef0-4c8b-a8b6-b60c25356b7b",
      "units": 2
    }
  ]
}
```

# GET /v1/invoices

**Example**

```bash
curl --request GET 'http://localhost:5000/v1/invoices'
```

**Response**

```json
{
  "invoices": [
    {
      "id": "45e4bfa2-79ac-4778-af9c-ca7bed0ef430",
      "invoice_date": "Wed, 23 Mar 2022 00:25:09 GMT"
    },
    {
      "id": "256aae12-5c7f-4e2e-bfff-47cfcb7e4db5",
      "invoice_date": "Wed, 23 Mar 2022 00:25:17 GMT"
    }
  ]
}
```

# POST /v1/invoices/:id

**Required keys**

- units: integer
- description: string
- amount: number

**Example**

```bash
curl --request POST 'http://localhost:5000/v1/invoices/256aae12-5c7f-4e2e-bfff-47cfcb7e4db5' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "units": 2,
        "description": "foo",
        "amount": 1
    },
    {
        "units": 2,
        "description": "bar",
        "amount": 1.2
    }
]'
```

**Response**

```json
{
  "id": "256aae12-5c7f-4e2e-bfff-47cfcb7e4db5",
  "invoice_date": "Wed, 23 Mar 2022 00:25:17 GMT",
  "invoice_items": [
    {
      "amount": 1.0,
      "description": "foo",
      "id": "9cadaab0-e7b6-414c-bd8b-b613f52ff47c",
      "units": 2
    },
    {
      "amount": 1.2,
      "description": "bar",
      "id": "1c9e72f8-cef0-4c8b-a8b6-b60c25356b7b",
      "units": 2
    }
  ]
}
```

# GET /v1/invoices/:id

**Example**

```bash
curl --request GET 'http://localhost:5000/v1/invoices/45e4bfa2-79ac-4778-af9c-ca7bed0ef430'
```

**Response**

```json
{
  "id": "256aae12-5c7f-4e2e-bfff-47cfcb7e4db5",
  "invoice_date": "Wed, 23 Mar 2022 00:25:17 GMT",
  "invoice_items": [
    {
      "amount": 1.0,
      "description": "foo",
      "id": "9cadaab0-e7b6-414c-bd8b-b613f52ff47c",
      "units": 2
    },
    {
      "amount": 1.2,
      "description": "bar",
      "id": "1c9e72f8-cef0-4c8b-a8b6-b60c25356b7b",
      "units": 2
    }
  ]
}
```

# Notes:

- I did not implement pagination for list all invoices endpoint
- Using string for `amount` column in `InvoiceItem` model for lessless storage since sqlite+pysqlite does not support Decimal objects natively.
