import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
)
from sqlalchemy.orm import relationship
from eastridge.db import Base


def generate_uuid():
    return str(uuid.uuid4())


class Invoice(Base):
    __tablename__ = "invoice"
    id = Column(String, primary_key=True, default=generate_uuid)
    invoice_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Invoice(id='{self.id}', invoice_date='{self.invoice_date}')>"


class InvoiceItem(Base):
    __tablename__ = "invoice_item"
    id = Column(String, primary_key=True, default=generate_uuid)
    units = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)

    invoice_id = Column(String, ForeignKey("invoice.id"), nullable=False)
    invoice = relationship("Invoice", backref="invoice_items", lazy=True)

    def __repr__(self):
        return f"<InvoiceItem(id='{self.id}', units='{self.units}', description='{self.description}', amount='{self.amount}')>"
