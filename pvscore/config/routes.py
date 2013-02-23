#pylint: disable-msg=R0915

def crm_routes(config):
    adrt = config.add_route
    adrt('crm.login', '/crm')
    adrt('crm.login.post', '/crm/login')
    adrt('crm.login.logout', '/crm/logout')
    adrt('crm.login.customer', '/crm/customer_login')
    adrt('crm.login.customer_forgot_password', '/crm/customer_forgot_password')
    adrt('crm.login.customer_login_to_link', '/crm/customer_login_to_link/{key}/{link}')

    adrt('crm.campaign.list', '/crm/campaign/list')
    adrt('crm.campaign.new', '/crm/campaign/new')
    adrt('crm.campaign.edit', '/crm/campaign/edit/{campaign_id}')
    adrt('crm.campaign.save', '/crm/campaign/save')
    adrt('crm.campaign.search', '/crm/campaign/search')

    adrt('crm.appointment.list', '/crm/appointment/list')
    adrt('crm.appointment.new', '/crm/appointment/new')
    adrt('crm.appointment.edit', '/crm/appointment/edit/{appointment_id}')
    adrt('crm.appointment.new_for_customer', '/crm/appointment/new_for_customer/{customer_id}')
    adrt('crm.appointment.edit_for_customer', '/crm/appointment/edit_for_customer/{customer_id}/{appointment_id}')
    adrt('crm.appointment.save', '/crm/appointment/save')
    adrt('crm.appointment.search', '/crm/appointment/search')
    adrt('crm.appointment.show_search', '/crm/appointment/show_search')
    adrt('crm.appointment.month_view', '/crm/appointment/month_view/{year}/{month}')
    adrt('crm.appointment.day_view', '/crm/appointment/day_view/{year}/{month}/{day}')
    adrt('crm.appointment.this_day', '/crm/appointment/this_day')
    adrt('crm.appointment.tomorrow', '/crm/appointment/tomorrow')
    adrt('crm.appointment.this_month', '/crm/appointment/this_month')
    adrt('crm.appointment.show_appointments', '/crm/appointment/show_appointments/{customer_id}')

    adrt('crm.company.new', '/crm/company/new')
    adrt('crm.company.edit', '/crm/company/edit/{company_id}')
    adrt('crm.company.save', '/crm/company/save')
    adrt('crm.company.search', '/crm/company/search')
    adrt('crm.company.show_search', '/crm/company/show_search')
    adrt('crm.company.list', '/crm/company/list')
    adrt('crm.company.enterprise.list', '/crm/company/enterprise/list')
    adrt('crm.company.enterprise.new', '/crm/company/enterprise/new')
    adrt('crm.company.enterprise.edit', '/crm/company/enterprise/edit/{enterprise_id}')
    adrt('crm.company.enterprise.save', '/crm/company/enterprise/save')
    adrt('crm.company.enterprise.provision', '/crm/company/provision')
    adrt('crm.company.enterprise.quickstart', '/crm/company/quickstart')
    adrt('crm.company.enterprise.clearcache', '/crm/company/enterprise/clearcache')

    adrt('crm.product.new', '/crm/product/new')
    adrt('crm.product.edit', '/crm/product/edit/{product_id}')
    adrt('crm.product.show_barcode', '/crm/product/show_barcode/{product_id}')
    adrt('crm.product.save', '/crm/product/save')
    adrt('crm.product.search', '/crm/product/search')
    adrt('crm.product.list', '/crm/product/list')
    adrt('crm.product.json', '/crm/product/json/{product_id}/{campaign_id}')
    adrt('crm.product.barcodes', '/crm/product/barcodes')
    adrt('crm.product.ac.name', '/crm/product/autocomplete_by_name')
    adrt('crm.product.show_orders', '/crm/product/show_orders/{product_id}')
    adrt('crm.product.show_sales', '/crm/product/show_sales/{product_id}')
    adrt('crm.product.show_purchases', '/crm/product/show_purchases/{product_id}')
    adrt('crm.product.show_history', '/crm/product/show_history/{product_id}')
    adrt('crm.product.show_returns', '/crm/product/show_returns/{product_id}')
    adrt('crm.product.show_status_dialog', '/crm/product/show_status_dialog/{product_id}/{status_id}')
    adrt('crm.product.save_status', '/crm/product/save_status')
    adrt('crm.product.show_inventory', '/crm/product/show_inventory')
    adrt('crm.product.save_inventory', '/crm/product/save_inventory')
    adrt('crm.product.inventory_list', '/crm/product/inventory_list')
    adrt('crm.product.delete', '/crm/product/delete/{product_id}')
    adrt('crm.product.delete_picture', '/crm/product/delete_picture/{product_id}/{asset_id}')
    adrt('crm.product.upload_picture', '/crm/product/upload_picture/{product_id}')

    adrt('crm.product.category.new', '/crm/product/category/new')
    adrt('crm.product.category.edit', '/crm/product/category/edit/{category_id}')
    adrt('crm.product.category.save', '/crm/product/category/save')
    adrt('crm.product.category.list', '/crm/product/category/list')

    adrt('crm.communication.new', '/crm/communication/new')
    adrt('crm.communication.edit', '/crm/communication/edit/{comm_id}')
    adrt('crm.communication.save', '/crm/communication/save')
    adrt('crm.communication.list', '/crm/communication/list')
    adrt('crm.communication.send_comm_dialog', '/crm/communication/send_comm_dialog')
    adrt('crm.communication.send_customer_comm', '/crm/communication/send_customer_comm/{customer_id}/{comm_id}')
    adrt('crm.communication.view_comm_dialog', '/crm/communication/view_comm_dialog/{customer_id}/{comm_id}')

    adrt('crm.users.new', '/crm/users/new')
    adrt('crm.users.edit', '/crm/users/edit/{user_id}')
    adrt('crm.users.edit_current', '/crm/users/edit_current')
    adrt('crm.users.save', '/crm/users/save')
    adrt('crm.users.save_password', '/crm/users/save_password')
    adrt('crm.users.search', '/crm/users/search')
    adrt('crm.users.list', '/crm/users/list')

    adrt('crm.event.new', '/crm/event/new')
    adrt('crm.event.edit', '/crm/event/edit/{event_id}')
    adrt('crm.event.save', '/crm/event/save')
    adrt('crm.event.search', '/crm/event/search')
    adrt('crm.event.list', '/crm/event/list')

    adrt('crm.phase.new', '/crm/phase/new')
    adrt('crm.phase.edit', '/crm/phase/edit/{phase_id}')
    adrt('crm.phase.save', '/crm/phase/save')
    adrt('crm.phase.search', '/crm/phase/search')
    adrt('crm.phase.list', '/crm/phase/list')


    adrt('crm.report.new', '/crm/report/new')
    adrt('crm.report.edit', '/crm/report/edit/{report_id}')
    adrt('crm.report.show', '/crm/report/show/{report_id}')
    adrt('crm.report.list', '/crm/report/list')
    adrt('crm.report.save', '/crm/report/save')
    adrt('crm.report.results', '/crm/report/results/{report_id}')
    adrt('crm.report.export', '/crm/report/results_export/{report_id}')

    adrt('crm.purchase.vendor.new', '/crm/purchase/vendor/new')  #, controller='crm/purchase', action='new_vendor')
    adrt('crm.purchase.vendor.edit', '/crm/purchase/vendor/edit/{vendor_id}')  #controller='crm/purchase', action='edit_vendor')
    adrt('crm.purchase.vendor.list', '/crm/purchase/vendor/list')  #, controller='crm/purchase', action='list_vendors')
    adrt('crm.purchase.vendor.save', '/crm/purchase/vendor/save')  #, controller='crm/purchase', action='save_vendor')
    adrt('crm.purchase.new', '/crm/purchase/new')  #, controller='crm/purchase', action='new')
    adrt('crm.purchase.edit', '/crm/purchase/edit/{purchase_order_id}')  #, controller='crm/purchase', action='edit')
    adrt('crm.purchase.list', '/crm/purchase/list')  #, controller='crm/purchase', action='list')
    adrt('crm.purchase.save', '/crm/purchase/save')  #, controller='crm/purchase', action='save')
    adrt('crm.purchase.search', '/crm/purchase/search')
    adrt('crm.purchase.show_search', '/crm/purchase/show_search')
    adrt('crm.purchase.order_item_json', '/crm/purchase/order_item_json/{purchase_order_id}/{order_item_id}')  #, controller='crm/purchase', action='order_item_json')
    adrt('crm.purchase.save_purchase_order_item', '/crm/purchase/save_purchase_order_item/{purchase_order_id}')  #, controller='crm/purchase', action='save_purchase_order_item')
    adrt('crm.purchase.delete_purchase_order_item', '/crm/purchase/delete_purchase_order_item/{purchase_order_id}/{order_item_id}')  #, controller='crm/purchase', action='delete_purchase_order_item')
    adrt('crm.purchase.show_history', '/crm/purchase/show_history/{purchase_order_id}')  #, controller='crm/purchase', action='show_history')
    adrt('crm.purchase.save_status', '/crm/purchase/save_status/{purchase_order_id}')  #, controller='crm/purchase', action='save_status')
    adrt('crm.purchase.complete', '/crm/purchase/complete/{purchase_order_id}')  #, controller='crm/purchase', action='complete')
    adrt('crm.purchase.complete_item', '/crm/purchase/complete_item/{purchase_order_id}/{order_item_id}')  #, controller='crm/purchase', action='complete_item')

    adrt('crm.customer.purchase_cart', '/crm/customer/purchase_cart')
    adrt('crm.customer.new', '/crm/customer/new')
    adrt('crm.customer.edit', '/crm/customer/edit/{customer_id}')
    adrt('crm.customer.editbye', '/crm/customer/edit_by_email/{customer_id}/{enterprise_id}')
    adrt('crm.customer.save', '/crm/customer/save')
    adrt('crm.customer.delete', '/crm/customer/delete/{customer_id}')
    adrt('crm.customer.search', '/crm/customer/search')
    adrt('crm.customer.show_search', '/crm/customer/show_search')
    adrt('crm.customer.edit_billing', '/crm/customer/edit_billing/{customer_id}')
    adrt('crm.customer.edit_billing_dialog', '/crm/customer/edit_billing_dialog/{customer_id}')
    adrt('crm.customer.apply_payment_dialog', '/crm/customer/apply_payment_dialog/{customer_id}/{order_id}')
    adrt('crm.customer.apply_payment', '/crm/customer/apply_payment/{customer_id}/{order_id}')
    adrt('crm.customer.return_item_dialog', '/crm/customer/return_item_dialog/{customer_id}/{order_id}/{order_item_id}')
    adrt('crm.customer.return_item', '/crm/customer/return_item/{customer_id}/{order_id}/{order_item_id}')
    adrt('crm.customer.add_order', '/crm/customer/add_order/{customer_id}')
    adrt('crm.customer.add_order_and_apply', '/crm/customer/add_order_and_apply/{customer_id}/{pmt_method}')
    adrt('crm.customer.add_order_dialog', '/crm/customer/add_order_dialog/{customer_id}')
    adrt('crm.customer.add_order_item', '/crm/customer/add_order/{customer_id}/{order_id}')
    adrt('crm.customer.add_order_item_dialog', '/crm/customer/add_order_item_dialog/{customer_id}/{order_id}')
    adrt('crm.customer.cancel_order_dialog', '/crm/customer/cancel_order_dialog/{customer_id}/{order_id}')
    adrt('crm.customer.cancel_order', '/crm/customer/cancel_order/{customer_id}/{order_id}')
    adrt('crm.customer.edit_order', '/crm/customer/edit_order/{customer_id}/{order_id}')
    adrt('crm.customer.edit_order_dialog', '/crm/customer/edit_order_dialog/{customer_id}/{order_id}')
    adrt('crm.customer.show_orders', '/crm/customer/show_orders/{customer_id}')
    adrt('crm.customer.show_history', '/crm/customer/show_history/{customer_id}')
    adrt('crm.customer.show_attributes', '/crm/customer/show_attributes/{customer_id}')
    adrt('crm.customer.show_appointments', '/crm/customer/show_appointments/{customer_id}')
    adrt('crm.customer.show_billings', '/crm/customer/show_billings/{customer_id}')
    adrt('crm.customer.show_billing_dialog', '/crm/customer/show_billing_dialog/{customer_id}/{journal_id}')
    adrt('crm.customer.autocomplete.name', '/crm/customer/autocomplete')
    adrt('crm.customer.show_summary', '/crm/customer/show_summary/{customer_id}')
    adrt('crm.customer.self_change_password', '/crm/customer/self_change_password')
    adrt('crm.customer.self_save', '/crm/customer/self_save')
    adrt('crm.customer.self_cancel_order', '/crm/customer/self_cancel_order')
    adrt('crm.customer.self_save_billing', '/crm/customer/self_save_billing')
    adrt('crm.customer.signup', '/crm/customer/signup')
    adrt('crm.customer.signup_and_purchase', '/crm/customer/signup_and_purchase')
    adrt('crm.customer.signup_free', '/crm/customer/signup_free')
    adrt('crm.customer.cancel_billing', '/crm/customer/cancel_billing/{customer_id}/{journal_id}')
    adrt('crm.customer.check_duplicate_email', '/crm/customer/check_duplicate_email/{email}')
    adrt('crm.customer.save_and_purchase', '/crm/customer/save_and_purchase')
    adrt('crm.customer.status_dialog', '/crm/customer/status_dialog/{customer_id}')
    adrt('crm.customer.show_status_dialog', '/crm/customer/show_status_dialog/{customer_id}/{status_id}')
    adrt('crm.customer.save_status', '/crm/customer/save_status/{customer_id}')
    adrt('crm.customer.get_balance', '/crm/customer/get_balance/{customer_id}')
    adrt('crm.customer.self_get_balance', '/crm/customer/self_get_balance/{customer_id}')
    adrt('crm.customer.contact', '/crm/customer/contact')

    adrt('cms.site.new', '/cms/site/new')
    adrt('cms.site.edit', '/cms/site/edit/{site_id}')
    adrt('cms.site.save', '/cms/site/save')
    adrt('cms.site.list', '/cms/site/list')
    adrt('cms.site.exception', '/cms/site/exception')

    adrt('cms.content.new', '/cms/content/new/{site_id}')
    adrt('cms.content.edit', '/cms/content/edit/{site_id}/{content_id}')
    adrt('cms.content.save', '/cms/content/save')
    adrt('cms.content.list', '/cms/content/list/{site_id}')

    adrt('crm.listing.remove', '/crm/listing/remove/{listing_id}')
    adrt('crm.listing.json.get', '/crm/listing/json_get')
    adrt('crm.listing.json', '/crm/listing/json/{listing_id}')
    adrt('crm.listing.show_add_picture', '/crm/listing/show_add_picture')
    adrt('crm.listing.save', '/crm/listing/save')
    adrt('crm.listing.upload', '/crm/listing/upload/{listing_id}/{hash}')

    # ecom routes
    adrt('ecom.site.cart.default', '/cart')
    adrt('ecom.site.cart', '/cart/{page}')
    adrt('ecom.site.cart.add', '/ecom/cart/add/{product_id}/{quantity}')
    adrt('ecom.site.cart.update', '/ecom/cart/update/{product_id}/{quantity}')
    adrt('ecom.site.cart.clear', '/ecom/cart/clear')
    adrt('ecom.site.cart.remove', '/ecom/cart/remove/{product_id}')
    adrt('ecom.site.cart.checkout.default', '/checkout')
    adrt('ecom.site.cart.checkout', '/checkout/{page}')
    adrt('ecom.site.cart.save_shipping', '/ecom/cart/save_shipping')


    adrt('ecom.site.product.default', '/product/{product_id}')
    adrt('ecom.site.product.named', '/product/{name}/{product_id}')
    adrt('ecom.site.product', '/product/{name}/{product_id}/{page}')

    adrt('ecom.site.products.default', '/products/{subset}')
    adrt('ecom.site.products', '/products/{subset}/{page}')

    adrt('ecom.site.search.default', '/ecom/search')
    adrt('ecom.site.search', '/ecom/search/{page}')

    adrt('ecom.site.category.default', '/category/{category_id}')
    adrt('ecom.site.category.named', '/category/{name}/{category_id}')
    adrt('ecom.site.category', '/category/{name}/{category_id}/{page}')

    adrt('ecom.site.login.default', '/ecom/login')
    adrt('ecom.site.login', '/ecom/login/{page}')

    adrt('ecom.site.page', '/ecom/page/{page}')
    adrt('ecom.site.content.default', '/ecom/content/{content_name}/{page}')
    adrt('ecom.site.content', '/ecom/content/{content_name}')


    adrt('crm.dashboard', '/crm/dashboard')


    # KB: [2011-09-02]: Don't let /test into the nginx proxying namespace.
    adrt('test.1', '/tsst/tsst_validate')
    adrt('test.2', '/tsst/tsst_admin_link')
    adrt('test.3', '/tsst/tsst_float')
    adrt('test.4', '/tsst/tsst_int')
    adrt('test.5', '/tsst/tsst_string')
    adrt('test.6', '/tsst/tsst_number')
    adrt('test.7', '/tsst/tsst_equals')
    adrt('test.8', '/tsst/tsst_redirto')
    adrt('test.9', '/tsst/tsst_redirto_post')
    adrt('test.10', '/tsst/tsst_customer_sidebar_link')
    adrt('test.11', '/tsst/tsst_validate2')

