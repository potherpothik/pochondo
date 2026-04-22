from odoo import _, api, fields, models
from odoo.exceptions import UserError


class BarcodeInventoryWizard(models.TransientModel):
    _name = "shop.barcode.inventory.wizard"
    _description = "Barcode Inventory Adjustment Wizard"

    product_id = fields.Many2one("product.product", string="Product", required=True)
    barcode = fields.Char(string="Barcode", required=True)
    location_id = fields.Many2one(
        "stock.location",
        string="Location",
        domain=[("usage", "=", "internal")],
        required=True,
        default=lambda self: self._default_location_id(),
    )
    quantity_delta = fields.Float(string="Quantity Change", required=True, default=1.0)
    note = fields.Text(string="Notes")

    @api.model
    def _default_location_id(self):
        location = self.env.ref("stock.stock_location_stock", raise_if_not_found=False)
        return location.id if location else False

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id and not self.barcode:
            self.barcode = self.product_id.barcode

    @api.onchange("barcode")
    def _onchange_barcode(self):
        if self.barcode and not self.product_id:
            product = self.env["product.product"].search([("barcode", "=", self.barcode)], limit=1)
            if product:
                self.product_id = product

    def action_apply_adjustment(self):
        self.ensure_one()
        product = self.product_id
        if not product and self.barcode:
            product = self.env["product.product"].search([("barcode", "=", self.barcode)], limit=1)
        if not product:
            raise UserError(_("Select a product or scan a known barcode."))
        if self.barcode != product.barcode:
            raise UserError(_("Scanned barcode does not match the selected product barcode."))
        if not self.quantity_delta:
            raise UserError(_("Quantity change must not be zero."))
        current_qty = product.with_context(location=self.location_id.id).qty_available
        if current_qty + self.quantity_delta < 0:
            raise UserError(_("Resulting quantity cannot be negative."))
        self.env["stock.quant"].sudo()._update_available_quantity(
            product,
            self.location_id,
            self.quantity_delta,
        )
        new_qty = product.with_context(location=self.location_id.id).qty_available

        self.env["shop.inventory.log"].create_from_stock_change(
            product=product,
            quantity_delta=self.quantity_delta,
            quantity_after=new_qty,
            operation_type="barcode_adjustment",
            note=self.note or _("Adjusted through barcode wizard."),
            location=self.location_id,
        )
        return {"type": "ir.actions.act_window_close"}
