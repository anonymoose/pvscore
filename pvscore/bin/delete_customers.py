# python ../pvscore/pvscore/bin/delete_customers.py wm wm "where customer_id > 5000"
import psycopg2, sys

def get_ids(cur, sql):
    cur.execute(sql)
    return [item[0] for item in cur.fetchall()]


def doit(conn, cur, sql):
    print sql
    cur.execute(sql)
    

def full_delete(conn, cur, customer_id):
    doit(conn, cur, "delete from core_asset where status_id in (select status_id from core_status where customer_id = '%s')" % customer_id)
    doit(conn, cur, "delete from crm_billing_history where customer_id = '%s'" % customer_id)
    doit(conn, cur, "delete from crm_product_inventory_journal where return_id in (select return_id from crm_product_return where journal_id in (select journal_id from crm_journal where customer_id = '%s'))" % customer_id)
    doit(conn, cur, "delete from crm_product_return where journal_id in (select journal_id from crm_journal where customer_id = '%s')" % customer_id)
    doit(conn, cur, "delete from crm_journal where customer_id = '%s'" % customer_id)
    doit(conn, cur, "delete from crm_product_inventory_journal where order_item_id in (select order_item_id from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id = '%s'))" % customer_id)
    doit(conn, cur, "delete from crm_oi_terms_acceptance where order_id in (select order_id from crm_customer_order where customer_id = '%s')" % customer_id)
    doit(conn, cur, "delete from wm_ireport_order where order_id in (select order_id from crm_customer_order where customer_id = '%s')" % customer_id)
    doit(conn, cur, "delete from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id = '%s')" % customer_id)
    doit(conn, cur, "delete from crm_customer_order where customer_id = '%s'" % customer_id)
    #doit(conn, cur, "delete from pvs_listing where customer_id = #'%s'" % customer_id)
    doit(conn, cur, "update crm_customer set status_id = null where customer_id = '%s'" % customer_id)
    doit(conn, cur, "delete from core_status where customer_id = '%s'" % customer_id)
    doit(conn, cur, "delete from crm_billing_history where customer_id = '%s'" % customer_id)
    doit(conn, cur, "delete from wm_portfolio where customer_id = '%s'" % customer_id)
    doit(conn, cur, "delete from wm_customer_holding where customer_id = '%s'" % customer_id)
    doit(conn, cur, "delete from wm_ireport_view_log where customer_id = '%s'" % customer_id)
    billing_ids = get_ids(cur, "select billing_id from crm_customer where customer_id = '%s'" % customer_id)
    doit(conn, cur, "delete from crm_customer where customer_id = '%s'" % customer_id)
    for bill_id in billing_ids:
        if bill_id:
            doit(conn, cur, "delete from crm_billing where billing_id = '%s'" % bill_id)


if __name__ == '__main__':
    dbname = sys.argv[1]
    entid = sys.argv[2]
    where = sys.argv[3]

    conn = psycopg2.connect("dbname={dbname} user={dbname} password={dbname} host=localhost".format(dbname=dbname))
    cur = conn.cursor()

    cids = get_ids(cur, "select customer_id from crm_customer %s" % where)
    lcids = len(cids)

    for i, cid in enumerate(cids):
        print '%s %s/%s' % (cid, i, lcids)
        full_delete(conn, cur, cid)
        conn.commit()
