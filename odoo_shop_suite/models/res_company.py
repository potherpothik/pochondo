from odoo import _, api, fields, models
from odoo.tools import float_compare


class ResCompany(models.Model):
    _inherit = "res.company"

    shop_suite_low_stock_threshold = fields.Float(
        string="Shop Suite Low Stock Threshold",
        default=10.0,
        help="Products below this quantity are included in low-stock monitoring.",
    )
    shop_suite_stock_alert_partner_ids = fields.Many2many(
        "res.partner",
        "res_company_shop_suite_alert_partner_rel",
        "company_id",
        "partner_id",
        string="Shop Suite Stock Alert Recipients",
    )

    def _shop_suite_get_stockable_products(self):
        self.ensure_one()
        return self.env["product.product"].search(
            [
                ("company_id", "in", [False, self.id]),
                ("detailed_type", "=", "product"),
                ("active", "=", True),
            ]
        )

    def _shop_suite_find_low_stock_products(self):
        self.ensure_one()
        threshold = self.shop_suite_low_stock_threshold
        products = self._shop_suite_get_stockable_products()
        return products.filtered(lambda p: float_compare(p.qty_available, threshold, precision_rounding=p.uom_id.rounding) < 0)

    @api.model
    def cron_shop_suite_low_stock_summary(self):
        companies = self.search([])
        for company in companies:
            low_stock_products = company._shop_suite_find_low_stock_products()
            if not low_stock_products:
                continue
            if not company.shop_suite_stock_alert_partner_ids:
                continue

            body_lines = [
                _("<p>The following products are below the configured stock threshold:</p>"),
                "<ul>",
            ]
            for product in low_stock_products[:100]:
                body_lines.append(
                    _("<li><strong>%s</strong>: Available %s (Threshold %s)</li>")
                    % (
                        product.display_name,
                        product.qty_available,
                        company.shop_suite_low_stock_threshold,
                    )
                )
            body_lines.append("</ul>")

            recipient_emails = company.shop_suite_stock_alert_partner_ids.mapped("email")
            recipient_emails = [email for email in recipient_emails if email]
            if not recipient_emails:
                continue

            mail_values = {
                "subject": _("Low Stock Summary - %s") % company.name,
                "body_html": "".join(body_lines),
                "email_to": ",".join(recipient_emails),
                "auto_delete": True,
            }
            self.env["mail.mail"].sudo().create(mail_values).send()
