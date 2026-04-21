from odoo import _, models
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_open_barcode_inventory_wizard(self):
        self.ensure_one()
        if not self.barcode:
            raise UserError(_("This product has no barcode. Please add one before using barcode inventory update."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Barcode Inventory Update"),
            "res_model": "shop.barcode.inventory.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_product_id": self.id,
                "default_barcode": self.barcode,
            },
        }
