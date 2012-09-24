#pylint: disable-msg=R0915

def crm_routes(config):
    adrt = config.add_route
    adrt('crm.login', '/crm')
    adrt('crm.login.post', '/crm/login')
    adrt('crm.login.logout', '/crm/logout')
    adrt('crm.login.customer', '/crm/customer_login')

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

    adrt('crm.product.new', '/crm/product/new') # ='crm/product', action='new')
    adrt('crm.product.edit', '/crm/product/edit/{product_id}') # ='crm/product', action='edit')
    adrt('crm.product.show_barcode', '/crm/product/show_barcode/{product_id}') # ='crm/product', action='show_barcode')
    adrt('crm.product.save', '/crm/product/save') # ='crm/product', action='save')
    adrt('crm.product.search', '/crm/product/search') # ='crm/product', action='search')
    adrt('crm.product.list', '/crm/product/list') # ='crm/product', action='list')
    adrt('crm.product.json', '/crm/product/json/{product_id}/{campaign_id}') # ='crm/product', action='json')
    adrt('crm.product.barcodes', '/crm/product/barcodes') # ='crm/product', action='barcodes')
    adrt('crm.product.ac.name', '/crm/product/autocomplete_by_name') # ='crm/product', action='autocomplete_by_name')
    adrt('crm.product.show_orders', '/crm/product/show_orders/{product_id}') # ='crm/product', action='show_orders')
    adrt('crm.product.show_sales', '/crm/product/show_sales/{product_id}') # ='crm/product', action='show_sales')
    adrt('crm.product.show_purchases', '/crm/product/show_purchases/{product_id}') # ='crm/product', action='show_purchases')
    adrt('crm.product.show_history', '/crm/product/show_history/{product_id}') # ='crm/product', action='show_history')
    adrt('crm.product.show_returns', '/crm/product/show_returns/{product_id}') # ='crm/product', action='show_returns')
    adrt('crm.product.show_status_dialog', '/crm/product/show_status_dialog/{product_id}/{status_id}') # ='crm/product', action='show_status_dialog')
    adrt('crm.product.save_status', '/crm/product/save_status') # ='crm/product', action='save_status')
    adrt('crm.product.show_inventory', '/crm/product/show_inventory') # ='crm/product', action='show_inventory')
    adrt('crm.product.save_inventory', '/crm/product/save_inventory') # ='crm/product', action='save_inventory')
    adrt('crm.product.inventory_list', '/crm/product/inventory_list') # ='crm/product', action='inventory_list')

    adrt('crm.product.category.new', '/crm/product/category/new') # ='crm/category', action='new')
    adrt('crm.product.category.edit', '/crm/product/category/edit/{category_id}') # ='crm/category', action='edit')
    adrt('crm.product.category.save', '/crm/product/category/save') # ='crm/category', action='save')
    adrt('crm.product.category.list', '/crm/product/category/list') # ='crm/category', action='list')

    adrt('crm.communication.new', '/crm/communication/new') #, controller='crm/communication', action='new')
    adrt('crm.communication.edit', '/crm/communication/edit/{comm_id}') #, controller='crm/communication', action='edit')
    adrt('crm.communication.save', '/crm/communication/save') #, controller='crm/communication', action='save')
    adrt('crm.communication.list', '/crm/communication/list') #, controller='crm/communication', action='list')
    adrt('crm.communication.send_comm_dialog', '/crm/communication/send_comm_dialog') #, controller='crm/communication', action='send_comm_dialog')
    adrt('crm.communication.send_customer_comm', '/crm/communication/send_customer_comm/{customer_id}/{comm_id}') #, controller='crm/communication', action='send_customer_comm')
    adrt('crm.communication.view_comm_dialog', '/crm/communication/view_comm_dialog/{customer_id}/{comm_id}') #, controller='crm/communication', action='view_comm_dialog')

    adrt('crm.users.new', '/crm/users/new') #controller='crm/users', action='new')
    adrt('crm.users.edit', '/crm/users/edit/{username}') #controller='crm/users', action='edit')
    adrt('crm.users.edit_current', '/crm/users/edit_current') #controller='crm/users', action='edit_current')
    adrt('crm.users.save', '/crm/users/save') #controller='crm/users', action='save')
    adrt('crm.users.save_password', '/crm/users/save_password') #controller='crm/users', action='save_password')
    adrt('crm.users.search', '/crm/users/search') #controller='crm/users', action='search')
    adrt('crm.users.list', '/crm/users/list') #controller='crm/users', action='list')

    adrt('crm.event.new', '/crm/event/new') #, controller='crm/event', action='new')
    adrt('crm.event.edit', '/crm/event/edit/{event_id}') #, controller='crm/event', action='edit')
    adrt('crm.event.save', '/crm/event/save') #, controller='crm/event', action='save')
    adrt('crm.event.search', '/crm/event/search') #, controller='crm/event', action='search')
    adrt('crm.event.list', '/crm/event/list') #, controller='crm/event', action='list')

    adrt('crm.report.new', '/crm/report/new') #, controller='crm/report', action='new')
    adrt('crm.report.edit', '/crm/report/edit/{report_id}') #, controller='crm/report', action='edit')
    adrt('crm.report.show', '/crm/report/show/{report_id}') #, controller='crm/report', action='show')
    adrt('crm.report.list', '/crm/report/list') #, controller='crm/report', action='list')
    adrt('crm.report.save', '/crm/report/save') #, controller='crm/report', action='save')
    adrt('crm.report.results', '/crm/report/results/{report_id}') #, controller='crm/report', action='results')
    adrt('crm.report.export', '/crm/report/results_export/{report_id}') #, controller='crm/report', action='results_export')
    
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

    adrt('crm.customer.new', '/crm/customer/new') # controller='crm/customer', action='new')
    adrt('crm.customer.edit', '/crm/customer/edit/{customer_id}') # controller='crm/customer', action='edit')
    adrt('crm.customer.editbye', '/crm/customer/edit_by_email/{customer_id}/{enterprise_id}') # controller='crm/customer', action='edit_by_email')
    adrt('crm.customer.save', '/crm/customer/save') # controller='crm/customer', action='save')
    adrt('crm.customer.delete', '/crm/customer/delete/{customer_id}') # controller='crm/customer', action='delete')
    adrt('crm.customer.search', '/crm/customer/search') #controller='crm/customer', action='search')
    adrt('crm.customer.show_search', '/crm/customer/show_search') # controller='crm/customer', action='search')
    adrt('crm.customer.edit_billing', '/crm/customer/edit_billing/{customer_id}') # controller='crm/customer', action='edit_billing')
    adrt('crm.customer.edit_billing_dialog', '/crm/customer/edit_billing_dialog/{customer_id}') # controller='crm/customer', action='edit_billing_dialog')
    adrt('crm.customer.apply_payment_dialog', '/crm/customer/apply_payment_dialog/{customer_id}/{order_id}') # controller='crm/customer', action='apply_payment_dialog')
    adrt('crm.customer.apply_payment', '/crm/customer/apply_payment/{customer_id}/{order_id}') # controller='crm/customer', action='apply_payment')
    adrt('crm.customer.return_item_dialog', '/crm/customer/return_item_dialog/{customer_id}/{order_id}/{order_item_id}') # controller='crm/customer', action='return_item_dialog')
    adrt('crm.customer.return_item', '/crm/customer/return_item/{customer_id}/{order_id}/{order_item_id}') # controller='crm/customer', action='return_item')
    adrt('crm.customer.add_order', '/crm/customer/add_order/{customer_id}') # controller='crm/customer', action='add_order')
    adrt('crm.customer.add_order_and_apply', '/crm/customer/add_order_and_apply/{customer_id}/{pmt_method}') # controller='crm/customer', action='add_order_and_apply')
    adrt('crm.customer.add_order_dialog', '/crm/customer/add_order_dialog/{customer_id}') # controller='crm/customer', action='add_order_dialog')
    adrt('crm.customer.add_order_item', '/crm/customer/add_order/{customer_id}/{order_id}') # controller='crm/customer', action='add_order_item')
    adrt('crm.customer.add_order_item_dialog', '/crm/customer/add_order_item_dialog/{customer_id}/{order_id}') # controller='crm/customer', action='add_order_item_dialog')
    adrt('crm.customer.cancel_order_dialog', '/crm/customer/cancel_order_dialog/{customer_id}/{order_id}')
    adrt('crm.customer.cancel_order', '/crm/customer/cancel_order/{customer_id}/{order_id}') #controller='crm/customer', action='cancel_order')
    adrt('crm.customer.edit_order', '/crm/customer/edit_order/{customer_id}/{order_id}') # controller='crm/customer', action='edit_order')
    adrt('crm.customer.edit_order_dialog', '/crm/customer/edit_order_dialog/{customer_id}/{order_id}') # controller='crm/customer', action='edit_order_dialog')
    adrt('crm.customer.show_orders', '/crm/customer/show_orders/{customer_id}') # controller='crm/customer', action='show_orders')
    adrt('crm.customer.show_history', '/crm/customer/show_history/{customer_id}') # controller='crm/customer', action='show_history')
    adrt('crm.customer.show_attributes', '/crm/customer/show_attributes/{customer_id}') # controller='crm/customer', action='show_attributes')
    adrt('crm.customer.show_appointments', '/crm/customer/show_appointments/{customer_id}') # controller='crm/customer', action='show_appointments')
    adrt('crm.customer.show_billings', '/crm/customer/show_billings/{customer_id}') # controller='crm/customer', action='show_billings')
    adrt('crm.customer.show_billing_dialog', '/crm/customer/show_billing_dialog/{customer_id}/{journal_id}') # controller='crm/customer', action='show_billing_dialog')
    adrt('crm.customer.autocomplete.name', '/crm/customer/autocomplete') # controller='crm/customer', action='autocomplete')
    adrt('crm.customer.show_summary', '/crm/customer/show_summary/{customer_id}') # controller='crm/customer', action='show_summary')
    adrt('crm.customer.self_change_password', '/crm/customer/self_change_password') # controller='crm/customer', action='self_change_password')
    adrt('crm.customer.self_save', '/crm/customer/self_save') # controller='crm/customer', action='self_save')
    adrt('crm.customer.self_cancel_order', '/crm/customer/self_cancel_order') # controller='crm/customer', action='self_cancel_order')
    adrt('crm.customer.self_save_billing', '/crm/customer/self_save_billing') # controller='crm/customer', action='self_save_billing')
    adrt('crm.customer.signup', '/crm/customer/signup') # controller='crm/customer', action='signup')
    adrt('crm.customer.signup_and_purchase', '/crm/customer/signup_and_purchase') # controller='crm/customer', action='signup_and_purchase')
    adrt('crm.customer.signup_free', '/crm/customer/signup_free') # controller='crm/customer', action='signup_free')
    adrt('crm.customer.cancel_billing', '/crm/customer/cancel_billing/{customer_id}/{journal_id}') # controller='crm/customer', action='cancel_billing')
    adrt('crm.customer.check_duplicate_email', '/crm/customer/check_duplicate_email/{email}') # controller='crm/customer', action='check_duplicate_email')
    adrt('crm.customer.save_and_purchase', '/crm/customer/save_and_purchase') # controller='crm/customer', action='save_and_purchase')
    adrt('crm.customer.status_dialog', '/crm/customer/status_dialog/{customer_id}') # controller='crm/customer', action='status_dialog')
    adrt('crm.customer.show_status_dialog', '/crm/customer/show_status_dialog/{customer_id}/{status_id}') # controller='crm/customer', action='show_status_dialog')
    adrt('crm.customer.save_status', '/crm/customer/save_status/{customer_id}') # controller='crm/customer', action='save_status')
    adrt('crm.customer.get_balance', '/crm/customer/get_balance/{customer_id}') # controller='crm/customer', action='get_balance')


    adrt('cms.site.new', '/cms/site/new') #, controller='cms/siteedit', action='new')
    adrt('cms.site.edit', '/cms/site/edit/{site_id}') #, controller='cms/siteedit', action='edit')
    adrt('cms.site.save', '/cms/site/save') #, controller='cms/siteedit', action='save')
    adrt('cms.site.list', '/cms/site/list') #, controller='cms/siteedit', action='list')

    adrt('crm.listing.remove', '/crm/listing/remove/{listing_id}')
    adrt('crm.listing.json', '/crm/listing/json/{listing_id}')
    adrt('crm.listing.show_add_picture', '/crm/listing/add_picture')
    adrt('crm.listing.save', '/crm/listing/save')
    adrt('crm.listing.upload', '/crm/listing/upload/{listing_id}')


    adrt('crm.dashboard', '/crm/dashboard')
