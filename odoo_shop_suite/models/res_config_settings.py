from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    shop_suite_low_stock_threshold = fields.Float(
        string="Low Stock Threshold",
        related="company_id.shop_suite_low_stock_threshold",
        readonly=False,
        help="Products with available quantity under this value are tracked as low stock.",
    )
    shop_suite_stock_alert_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Stock Alert Recipients",
        related="company_id.shop_suite_stock_alert_partner_ids",
        readonly=False,
        help="Contacts who should receive low-stock summary emails.",
    )
