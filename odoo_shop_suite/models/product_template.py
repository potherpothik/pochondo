from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    shop_suite_is_featured = fields.Boolean(
        string="Featured in Shop Showcase",
        help="Display this product in the custom animated storefront section.",
    )
    shop_suite_reorder_min_qty = fields.Float(
        string="Reorder Minimum Quantity",
        default=5.0,
        help="Target minimum quantity. Alerts are generated when stock goes below this value.",
    )
    shop_suite_reorder_target_qty = fields.Float(
        string="Reorder Target Quantity",
        default=20.0,
        help="Recommended quantity to replenish up to.",
    )
    shop_suite_barcode_required = fields.Boolean(
        string="Barcode Required",
        default=True,
        help="If enabled, this product should always carry a barcode for in-store operations.",
    )
    shop_suite_sku = fields.Char(
        string="Shop SKU",
        index=True,
        copy=False,
        help="Internal SKU used by the shop for reconciliation between online and in-store sales.",
    )

    @api.constrains("shop_suite_reorder_min_qty", "shop_suite_reorder_target_qty")
    def _check_reorder_levels(self):
        for product in self:
            if product.shop_suite_reorder_min_qty < 0 or product.shop_suite_reorder_target_qty < 0:
                raise ValidationError(_("Reorder levels must be positive or zero."))
            if product.shop_suite_reorder_target_qty < product.shop_suite_reorder_min_qty:
                raise ValidationError(
                    _("Reorder target quantity must be greater than or equal to reorder minimum quantity.")
                )

    @api.constrains("shop_suite_sku")
    def _check_unique_shop_sku(self):
        for product in self:
            if not product.shop_suite_sku:
                continue
            duplicate = self.search(
                [
                    ("id", "!=", product.id),
                    ("shop_suite_sku", "=", product.shop_suite_sku),
                ],
                limit=1,
            )
            if duplicate:
                raise ValidationError(
                    _("Shop SKU must be unique. '%s' is already used.") % product.shop_suite_sku
                )

