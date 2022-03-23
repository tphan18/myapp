# Endpoints

```text
    POST    /v1/invoices          Create an invoice with its items
     GET    /v1/invoices          List all invoices
    POST    /v1/invoices/:id      Add items with the given ID
     GET    /v1/invoices/:id      Get invoice with the given ID
```

# Notes:

- I did not implement pagination for list all invoices endpoint
- Using string for `amount` column in `InvoiceItem` model for lessless storage since sqlite+pysqlite does not support Decimal objects natively.
