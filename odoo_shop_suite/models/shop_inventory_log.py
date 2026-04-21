from odoo import api, fields, models


class ShopInventoryLog(models.Model):
    _name = "shop.inventory.log"
    _description = "Shop Inventory Operation Log"
    _order = "create_date desc, id desc"

    name = fields.Char(required=True, default="Inventory Operation")
    product_id = fields.Many2one("product.product", required=True, ondelete="cascade")
    user_id = fields.Many2one("res.users", required=True, default=lambda self: self.env.user)
    operation_type = fields.Selection(
        [
            ("manual_adjustment", "Manual Adjustment"),
            ("barcode_adjustment", "Barcode Adjustment"),
            ("auto_reorder", "Auto Reorder"),
        ],
        required=True,
        default="manual_adjustment",
    )
    quantity_delta = fields.Float(required=True)
    quantity_after = fields.Float(required=True)
    location_id = fields.Many2one("stock.location", string="Location")
    note = fields.Text()

    @api.model
    def create_from_stock_change(
        self,
        *,
        product,
        quantity_delta,
        quantity_after,
        operation_type="manual_adjustment",
        note="",
        location=None,
    ):
        return self.create(
            {
                "name": f"{product.display_name} - {operation_type.replace('_', ' ').title()}",
                "product_id": product.id,
                "quantity_delta": quantity_delta,
                "quantity_after": quantity_after,
                "operation_type": operation_type,
                "note": note,
                "location_id": location.id if location else False,
            }
        )
