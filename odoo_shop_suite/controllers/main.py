from odoo import http
from odoo.http import request


class ShopSuiteWebsite(http.Controller):
    @http.route(["/shop-suite"], type="http", auth="public", website=True, sitemap=True)
    def shop_suite_home(self, **kwargs):
        featured_products = (
            request.env["product.template"]
            .sudo()
            .search(
                [
                    ("sale_ok", "=", True),
                    ("is_published", "=", True),
                    ("shop_suite_is_featured", "=", True),
                ],
                limit=8,
            )
        )
        values = {
            "featured_products": featured_products,
            "top_categories": request.env["product.public.category"].sudo().search([], limit=6),
        }
        return request.render("odoo_shop_suite.website_shop_suite_landing", values)
