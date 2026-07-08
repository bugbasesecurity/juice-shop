from flask import Flask, request


app = Flask(__name__)


class InvoiceStore:
    def find(self, invoice_id):
        return {"id": invoice_id, "tenant_id": "tenant-a", "payment_id": "pay_123", "total": 100}

    def update(self, invoice_id, fields):
        return {"id": invoice_id, **fields}


class PaymentGateway:
    def refund(self, payment_id, amount):
        return {"payment_id": payment_id, "refunded": amount}


invoices = InvoiceStore()
payments = PaymentGateway()


@app.route("/tenants/<tenant_id>/invoices/<invoice_id>", methods=["GET"])
def read_invoice(tenant_id, invoice_id):
    invoice = invoices.find(invoice_id)
    return invoice


@app.route("/tenants/<tenant_id>/invoices/<invoice_id>/refund", methods=["POST"])
def refund_invoice(tenant_id, invoice_id):
    invoice = invoices.find(invoice_id)
    amount = float(request.json.get("amount", invoice["total"]))
    result = payments.refund(invoice["payment_id"], amount)
    invoices.update(invoice_id, {"status": "refunded"})
    return result
