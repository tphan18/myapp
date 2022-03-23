from flask import Blueprint

from eastridge.payload_schemas import INVOICE_ITEMS_SCHEMA
from eastridge.db import db_session
from eastridge.models import Invoice, InvoiceItem
from eastridge.utils import get_payloads

bp = Blueprint("invoices", __name__, url_prefix="/v1/invoices")


def save_invoice(invoice, invoice_items):
    for item in invoice_items:
        invoice_item = InvoiceItem(**item)
        invoice.invoice_items.append(invoice_item)

    db_session.add(invoice)
    db_session.commit()

    return None


@bp.route("", methods=["GET"])
def list_invoices():
    return {"invoices": [invoice.as_dict() for invoice in Invoice.query.all()]}


@bp.route("", methods=["POST"])
def create_invoice():
    payloads = get_payloads(INVOICE_ITEMS_SCHEMA)
    invoice = Invoice()
    save_invoice(invoice, payloads)

    return invoice.as_dict()


@bp.route("/<invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return {"error": "Invoice not found"}, 404

    return invoice.as_dict()


@bp.route("/<invoice_id>", methods=["POST"])
def update_invoice(invoice_id):
    payloads = get_payloads(INVOICE_ITEMS_SCHEMA)
    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return {"error": "Invoice not found"}, 404

    save_invoice(invoice, payloads)

    return invoice.as_dict()
