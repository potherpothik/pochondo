# Shop Suite for Odoo 19 Community

`odoo_shop_suite` is an end-to-end commerce extension that helps a business sell both online and in physical stores.

## Features

- Modern animated landing page at `/shop-suite`
- Featured product showcase integrated with `website_sale`
- Quick product creation wizard (name, prices, barcode, SKU, reorder levels, website publication)
- Barcode-based inventory adjustment wizard for in-store stock updates
- Inventory operation log for audit and reconciliation
- Low-stock summary cron email notifications
- Settings for stock threshold and alert recipients
- Product enhancements:
  - Shop SKU
  - reorder minimum and target quantities
  - featured flag
  - barcode required marker

## Required Odoo Apps

- Sales Management (`sale_management`)
- Inventory (`stock`)
- Barcode (`stock_barcode`)
- Website + eCommerce (`website`, `website_sale`)
- Discuss/Mail (`mail`)

## Installation

1. Place `odoo_shop_suite` in your custom addons path.
2. Restart Odoo.
3. Update apps list.
4. Install **Shop Suite for Odoo 19 Community**.

## Main User Flows

### 1) Add Products from UI (fast onboarding)

1. Go to **Shop Suite > Quick Product Onboarding**
2. Fill in product details (barcode/SKU/reorder levels optional but recommended)
3. Save to create a full `product.template` and open it immediately

### 2) Barcode Inventory Update

1. Open a storable product variant
2. Click **Barcode Inventory Update**
3. Scan/enter barcode, choose location, enter quantity delta (+/-)
4. Apply adjustment; entry is logged in **Inventory Operations Log**

### 3) Low Stock Monitoring

1. Open **Settings > Shop Suite**
2. Configure low-stock threshold and recipients
3. Daily cron sends summary email when products fall below threshold

### 4) Online Storefront

- Visit `/shop-suite` to view the custom hero + featured products + category highlights
- Shop button links directly to `/shop`

## Security

- Inventory logs + barcode wizard: Stock User group
- Quick product wizard + settings: Sales Manager group

## Notes

- This module is a production-grade foundation and can be extended for:
  - POS integration
  - payment/provider customization
  - purchase auto-replenishment rules
  - advanced multi-warehouse stock policies
