"""App models. """

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from eastridge.db import Base


def generate_uuid():
    return str(uuid.uuid4())


class Invoice(Base):
    __tablename__ = "invoice"
    id = Column(String, primary_key=True, default=generate_uuid)
    invoice_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    def get_invoice_items(self):
        return [
            {
                "id": invoice_item.id,
                "units": invoice_item.units,
                "description": invoice_item.description,
                "amount": float(invoice_item.amount),
            }
            for invoice_item in self.invoice_items
        ]

    def as_dict(self):
        return {
            "id": self.id,
            "invoice_date": self.invoice_date,
            "invoice_items": self.get_invoice_items(),
        }

    def __repr__(self):
        return f"<Invoice(id='{self.id}', invoice_date='{self.invoice_date}')>"


class InvoiceItem(Base):
    __tablename__ = "invoice_item"
    id = Column(String, primary_key=True, default=generate_uuid)
    units = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(String, nullable=False, default=str)

    invoice_id = Column(String, ForeignKey("invoice.id"), nullable=False)
    invoice = relationship("Invoice", backref="invoice_items", lazy=True)

    def __repr__(self):
        return f"<InvoiceItem(id='{self.id}', units='{self.units}', description='{self.description}', amount='{self.amount}')>"
