import psycopg2, sys

def get_ids(cur, sql):
    cur.execute(sql)
    return [item[0] for item in cur.fetchall()]


def doit(conn, cur, sql):
    print sql
    cur.execute(sql)
    conn.commit()
    

def full_delete(conn, cur, enterprise_id, is_new):
    company_ids = get_ids(cur, "select company_id from crm_company where enterprise_id = '%s'" % enterprise_id)
    campaign_ids = get_ids(cur, """select campaign_id from crm_campaign where
                                  company_id in (select company_id from crm_company where enterprise_id = '%s')""" % enterprise_id)

    customer_ids = get_ids(cur, """select customer_id from crm_customer where
                                  campaign_id in (select campaign_id from crm_campaign where
                                      company_id in (select company_id from crm_company where enterprise_id = '%s'))""" % enterprise_id)
    product_ids = get_ids(cur, """select product_id from crm_product where
                                 company_id in (select company_id from crm_company where enterprise_id = '%s')""" % enterprise_id)

    doit(conn, cur, "truncate table pvs_listing_favorite")
    doit(conn, cur, "truncate table pvs_listing_message");
    for customer_id in customer_ids:
        doit(conn, cur, "delete from core_asset where status_id in (select status_id from core_status where customer_id = '%s')" % customer_id)
        doit(conn, cur, "delete from crm_billing_history where customer_id = '%s'" % customer_id)
        doit(conn, cur, "delete from crm_product_inventory_journal where return_id in (select return_id from crm_product_return where journal_id in (select journal_id from crm_journal where customer_id = '%s'))" % customer_id)
        doit(conn, cur, "delete from crm_product_return where journal_id in (select journal_id from crm_journal where customer_id = '%s')" % customer_id)
        doit(conn, cur, "delete from crm_journal where customer_id = '%s'" % customer_id)
        doit(conn, cur, "delete from crm_product_inventory_journal where order_item_id in (select order_item_id from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id = '%s'))" % customer_id)
        doit(conn, cur, "delete from crm_oi_terms_acceptance where order_id in (select order_id from crm_customer_order where customer_id = '%s')" % customer_id)
        doit(conn, cur, "delete from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id = '%s')" % customer_id)
        doit(conn, cur, "delete from crm_customer_order where customer_id = '%s'" % customer_id)
        #doit(conn, cur, "delete from wm_portfolio where customer_id = '%s'" % customer_id)
        doit(conn, cur, "delete from pvs_listing where customer_id = '%s'" % customer_id)
        doit(conn, cur, "delete from pvs_listing_favorite where customer_id = '%s'" % customer_id)
        doit(conn, cur, "update crm_customer set status_id = null where customer_id = '%s'" % customer_id)
        doit(conn, cur, "delete from core_status where customer_id = '%s'" % customer_id)
        doit(conn, cur, "delete from crm_billing_history where customer_id = '%s'" % customer_id)
        billing_ids = get_ids(cur, "select billing_id from crm_customer where customer_id = '%s'" % customer_id)
        doit(conn, cur, "delete from crm_customer where customer_id = '%s'" % customer_id)
        for bill_id in billing_ids:
            if bill_id is not None:
                doit(conn, cur, "delete from crm_billing where billing_id = '%s'" % bill_id)

    for product_id in product_ids:
        doit(conn, cur, "delete from crm_product_return where product_id = '%s'" % product_id)
        doit(conn, cur, "delete from crm_product_category_join where product_id = '%s'" % product_id)
        doit(conn, cur, "delete from crm_product_child where parent_id = '%s'" % product_id)
        doit(conn, cur, "delete from crm_product_child where child_id = '%s'" % product_id)
        doit(conn, cur, "delete from crm_product_pricing where product_id = '%s'" % product_id)
        doit(conn, cur, "delete from crm_product_inventory_journal where product_id = '%s'" % product_id)
        doit(conn, cur, "delete from crm_purchase_order_item where product_id = '%s'" % product_id)
        doit(conn, cur, "delete from crm_order_item where product_id = '%s'" % product_id)
        doit(conn, cur, "delete from crm_product where product_id = '%s'" % product_id)
        
    for campaign_id in campaign_ids:
        doit(conn, cur, "delete from crm_product_pricing where campaign_id = '%s'" % campaign_id)
        
    doit(conn, cur, "update crm_company set default_campaign_id = null where enterprise_id = '%s'" % enterprise_id)
    for company_id in company_ids:
        doit(conn, cur, "delete from crm_product_category where company_id = '%s'" % company_id)
        doit(conn, cur, "delete from crm_report where company_id = '%s'" % company_id)
        doit(conn, cur, """delete from cms_content
                            where page_id in (select page_id from cms_page where site_id in
                                                  (select site_id from cms_site where company_id = '%s'))""" % company_id)
        doit(conn, cur, "delete from cms_page where site_id in (select site_id from cms_site where company_id = '%s')" % company_id)
        doit(conn, cur, "delete from cms_site where company_id = '%s'" % company_id)
        doit(conn, cur, "delete from crm_campaign where company_id = '%s'" % company_id)
        doit(conn, cur, "delete from crm_purchase_order where company_id = '%s'" % company_id)
        

    if is_new:
        user_ids = get_ids(cur, """select user_id from core_user where enterprise_id = '%s'""" % enterprise_id)
        doit(conn, cur, "delete from core_asset where enterprise_id = '%s'" % enterprise_id)
        for user_id in user_ids:
            doit(conn, cur, "delete from core_status where username = '%s'" % user_id)

    doit(conn, cur, "delete from crm_communication where enterprise_id = '%s'" % enterprise_id)
    doit(conn, cur, "delete from core_status where event_id in (select event_id from core_status_event where enterprise_id = '%s')" % enterprise_id)
    doit(conn, cur, "delete from core_status_event_reason where event_id in (select event_id from core_status_event where enterprise_id = '%s')" % enterprise_id)
    doit(conn, cur, "delete from core_status_event where enterprise_id = '%s'" % enterprise_id)
    doit(conn, cur, "delete from cms_template where enterprise_id = '%s'" % enterprise_id)
    doit(conn, cur, "delete from crm_company where enterprise_id = '%s'" % enterprise_id)
    #doit(conn, cur, 'update core_user set enterprise_id = null where enterprise_id = '%s'" % enterprise_id)
    doit(conn, cur, "delete from core_user where enterprise_id = '%s'" % enterprise_id)
    doit(conn, cur, "delete from crm_vendor where enterprise_id = '%s'" % enterprise_id)
    doit(conn, cur, "delete from crm_enterprise where enterprise_id = '%s'" % enterprise_id)


if __name__ == '__main__':
    dbname = sys.argv[1]
    entid = sys.argv[2]
    is_new = False
    if len(sys.argv) == 4:
        is_new = sys.argv[3]

    conn = psycopg2.connect("dbname={dbname} user={dbname} password={dbname} host=localhost".format(dbname=dbname))
    cur = conn.cursor()

    eids = get_ids(cur, "select enterprise_id, name from crm_enterprise where enterprise_id != '%s' order by enterprise_id desc" % entid)
    leids = len(eids)

    for i, eid in enumerate(eids):
        print '%s %s/%s' % (eid, i, leids)
        full_delete(conn, cur, eid, is_new)
        conn.commit()
