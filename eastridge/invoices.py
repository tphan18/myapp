"""Invoices module."""

from flask import Blueprint

from myapp.db import db_session
from myapp.models import Invoice, InvoiceItem
from myapp.payload_schemas import INVOICE_ITEMS_SCHEMA
from myapp.utils import get_payloads

bp = Blueprint("invoices", __name__, url_prefix="/v1/invoices")


def save_invoice(invoice, invoice_items):
    """Save invoice and invoice items.

    Args:
        invoice (Invoice): The Invoice object.
        invoice_items (list of InvoiceItems): List of InvoiceItem objects.

    Returns: None
    """
    for item in invoice_items:
        invoice_item = InvoiceItem(**item)
        invoice.invoice_items.append(invoice_item)

    db_session.add(invoice)
    db_session.commit()

    return None


@bp.route("", methods=["GET"])
def list_invoices():
    """List all invoices."""
    return {
        "invoices": [
            {"id": invoice.id, "invoice_date": invoice.invoice_date}
            for invoice in Invoice.query.all()
        ]
    }


@bp.route("", methods=["POST"])
def create_invoice():
    """Create an invoice."""
    payloads = get_payloads(INVOICE_ITEMS_SCHEMA)
    invoice = Invoice()
    save_invoice(invoice, payloads)

    return invoice.as_dict()


@bp.route("/<invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    """Get an invoice."""
    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return {"error": "Not found"}, 404

    return invoice.as_dict()


@bp.route("/<invoice_id>", methods=["POST"])
def update_invoice(invoice_id):
    """Update an invoice."""
    payloads = get_payloads(INVOICE_ITEMS_SCHEMA)
    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return {"error": "Not found"}, 404

    save_invoice(invoice, payloads)

    return invoice.as_dict()
