from odoo import models, fields, api
import base64
import qrcode
from io import BytesIO
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'
    po_number = fields.Char(string='P.O Number')
    delivery_note = fields.Char(string="Delivery Note")

    zatca_qr_code = fields.Binary("ZATCA QR", compute="_generate_zatca_qr", store=True)

    @api.depends('amount_total', 'amount_tax', 'invoice_date', 'partner_id', 'company_id', 'company_id.vat')
    def _generate_zatca_qr(self):
        for rec in self:
            if not rec.company_id or not rec.company_id.vat:
                rec.zatca_qr_code = False
                continue

            def _encode_field(tag, value):
                data = bytes([tag, len(value)]) + value.encode('utf-8')
                return data

            qr_bytes = b''.join([
                _encode_field(1, rec.company_id.name or ""),
                _encode_field(2, rec.company_id.vat or ""),
                _encode_field(3, rec.invoice_date.strftime('%Y-%m-%d %H:%M:%S') if rec.invoice_date else ""),
                _encode_field(4, str(rec.amount_total)),
                _encode_field(5, str(rec.amount_tax))
            ])

            qr_base64 = base64.b64encode(qr_bytes)
            qr_img = qrcode.make(qr_base64.decode())
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            qr_data = base64.b64encode(buffer.getvalue())
            rec.zatca_qr_code = qr_data


delivery_date = fields.Datetime(string="Delivery Date", compute="_compute_delivery_date", store=False)
def _compute_delivery_date(self):
    for move in self:
        delivery_date = False
        sale_lines = move.invoice_line_ids.mapped('sale_line_ids')
        if sale_lines:
            pickings = sale_lines.mapped('order_id').mapped('picking_ids').filtered(lambda p: p.state == 'done')
            if pickings:
                # Get last picking by date_done
                delivery_date = sorted(pickings, key=lambda p: p.date_done or p.scheduled_date)[-1].date_done
        move.delivery_date = delivery_date




