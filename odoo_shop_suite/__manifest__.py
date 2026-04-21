{
    "name": "Shop Suite for Odoo 19 Community",
    "version": "19.0.1.0.0",
    "summary": "Unified online and in-store commerce with barcode and inventory flows",
    "description": """
Shop Suite provides a production-ready starter for businesses that sell online and in physical shops.

Key capabilities:
* Professional animated storefront landing page
* Fast backend product onboarding from UI
* Barcode-based inventory adjustments
* Low-stock monitoring and daily notifications
* Dedicated dashboards and logs for operations teams
    """,
    "category": "Sales/Website",
    "author": "Cursor Cloud Agent",
    "website": "https://www.odoo.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "product",
        "sale_management",
        "stock",
        "stock_barcode",
        "website",
        "website_sale",
    ],
    "data": [
        "security/shop_suite_security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "views/shop_suite_menus.xml",
        "views/product_views.xml",
        "views/res_config_settings_views.xml",
        "views/shop_inventory_log_views.xml",
        "wizard/quick_product_create_wizard_views.xml",
        "wizard/barcode_inventory_wizard_views.xml",
        "views/website_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "odoo_shop_suite/static/src/css/shop_suite.css",
            "odoo_shop_suite/static/src/js/shop_suite.js",
        ],
    },
    "application": True,
    "installable": True,
}
