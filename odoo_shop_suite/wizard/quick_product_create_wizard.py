from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class QuickProductCreateWizard(models.TransientModel):
    _name = "shop.quick.product.create.wizard"
    _description = "Quick Product Create Wizard"

    name = fields.Char(required=True)
    list_price = fields.Float(required=True, default=0.0)
    standard_price = fields.Float(string="Cost", default=0.0)
    barcode = fields.Char()
    default_code = fields.Char(string="Internal Reference")
    shop_suite_sku = fields.Char(string="Shop SKU")
    detailed_type = fields.Selection(
        selection=[("consu", "Consumable"), ("service", "Service"), ("product", "Storable Product")],
        default="product",
        required=True,
    )
    categ_id = fields.Many2one("product.category", required=True, default=lambda self: self._default_category())
    shop_suite_reorder_min_qty = fields.Float(default=5.0)
    shop_suite_reorder_target_qty = fields.Float(default=20.0)
    shop_suite_is_featured = fields.Boolean(default=False)
    publish_on_website = fields.Boolean(default=True)

    @api.model
    def _default_category(self):
        category = self.env.ref("product.product_category_all", raise_if_not_found=False)
        return category.id if category else False

    @api.constrains("shop_suite_reorder_min_qty", "shop_suite_reorder_target_qty")
    def _check_reorder_levels(self):
        for wizard in self:
            if wizard.shop_suite_reorder_min_qty < 0 or wizard.shop_suite_reorder_target_qty < 0:
                raise ValidationError(_("Reorder levels must be positive or zero."))
            if wizard.shop_suite_reorder_target_qty < wizard.shop_suite_reorder_min_qty:
                raise ValidationError(
                    _("Reorder target quantity must be greater than or equal to reorder minimum quantity.")
                )

    def action_create_product(self):
        self.ensure_one()
        values = {
            "name": self.name,
            "list_price": self.list_price,
            "standard_price": self.standard_price,
            "barcode": self.barcode,
            "default_code": self.default_code,
            "shop_suite_sku": self.shop_suite_sku,
            "detailed_type": self.detailed_type,
            "categ_id": self.categ_id.id,
            "shop_suite_reorder_min_qty": self.shop_suite_reorder_min_qty,
            "shop_suite_reorder_target_qty": self.shop_suite_reorder_target_qty,
            "shop_suite_is_featured": self.shop_suite_is_featured,
            "is_published": self.publish_on_website,
        }
        template = self.env["product.template"].create(values)
        return {
            "type": "ir.actions.act_window",
            "name": _("Created Product"),
            "res_model": "product.template",
            "res_id": template.id,
            "view_mode": "form",
            "target": "current",
        }
