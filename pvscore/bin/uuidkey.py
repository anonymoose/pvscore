import psycopg2
import sys, os
import uuid
from pprint import pprint
from hashlib import md5
import pvscore.lib.util as util
import shutil

def list_tables(cur):
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    return [tname[0] for tname in cur.fetchall()]


def list_keys(cur, tablename, keytype):
    cur.execute("""
        SELECT
            tc.constraint_name, tc.table_name, kcu.column_name, 
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name 
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
        WHERE constraint_type = '%s KEY' AND tc.table_name='%s'""" % (keytype, tablename))
    return cur.fetchall()


def get_columns_of_type(cur, datatype):
    cur.execute("select table_name, column_name, data_type from information_schema.columns where data_type = '%s'" % datatype)
    return cur.fetchall()

def change_type(cur, table_name, column_name, totype):
    cur.execute("""alter table {tname} alter column {cname} set data type {totype}""".format(tname=table_name,
                                                                                             cname=column_name,
                                                                                             totype=totype))

def get_column_type(cur, table_name, column_name):
    cur.execute("""select data_type from information_schema.columns where
                   table_name = '%s' and column_name = '%s'""" % (table_name, column_name))
    return cur.fetchone()[0]


def add_uuid_col(cur, table_name, base_column_name):
    sql = "alter table {tname} add column {colbase}_uuid uuid".format(tname=table, colbase=base_column_name)
    print '    %s' % sql
    cur.execute(sql)


def get_pk_vals(cur, table_name, pk_col_name):
    cur.execute("select {col} from {tab}".format(col=pk_col_name, tab=table_name))
    return [val[0] for val in cur.fetchall()]


def get_old_and_new_pk_vals(cur, table_name, pk_col_name):
    cur.execute("select {col}, {col}_uuid from {tab}".format(col=pk_col_name, tab=table_name))
    return cur.fetchall()


def update_uuid_for_pk(cur, table_name, pk_col_name, pk_val):
    cur.execute("""update {tab} set {col}_uuid = '{uid}'
                    where {col} = {pk_val}""".format(tab=table_name,
                                                     uid=uuid.uuid4(),
                                                     col=pk_col_name,
                                                     pk_val=pk_val))
    

def set_foreign_uuid_val(cur, table, pk_col_name, pk_val, fk_col_name, foreign_table_name, foreign_column_name):
    sql = """update {table} set {fk_col_name}_uuid = (select {foreign_column_name}_uuid from {foreign_table_name}
                          where {foreign_column_name} = (select {fk_col_name} from {table} where {pk_col_name} = {pk_val}))
                                                         where {pk_col_name} = {pk_val} and {fk_col_name} is not null
                """.format(table=table,
                           pk_col_name=pk_col_name,
                           pk_val=pk_val,
                           fk_col_name=fk_col_name,
                           foreign_table_name=foreign_table_name,
                           foreign_column_name=foreign_column_name)
    cur.execute(sql)


def drop_constraint(cur, table, fk_constraint_name):
    sql = """alter table {table} drop constraint if exists {fk_constraint_name} CASCADE""".format(table=table, fk_constraint_name=fk_constraint_name)
    print sql
    cur.execute(sql)


def get_indexes(cur, table):
    sql = """select
            t.relname as table_name,
            i.relname as index_name,
            array_to_string(array_agg(a.attname), ', ') as column_names
        from
            pg_class t,
            pg_class i,
            pg_index ix,
            pg_attribute a
        where
            t.oid = ix.indrelid
            and i.oid = ix.indexrelid
            and a.attrelid = t.oid
            and a.attnum = ANY(ix.indkey)
            and t.relkind = 'r'
            and t.relname = '{table}'
            and i.relname not like '%_pkey'
        group by
            t.relname,
            i.relname
        order by
            t.relname,
            i.relname""".format(table=table)
    cur.execute(sql)
    return cur.fetchall()

def rename_uuid_col(cur, table, fk_col_name, is_pk=False):
    # http://blog.enricostahn.com/2010/06/11/postgresql-add-primary-key-to-an-existing-table.html
    cur.execute("alter table {table} drop column {fk_col_name}".format(table=table, fk_col_name=fk_col_name))
    cur.execute("alter table {table} rename column {fk_col_name}_uuid to {fk_col_name}".format(table=table, fk_col_name=fk_col_name))
    if is_pk:
        cur.execute("alter table {table} alter column {fk_col_name} set not null""".format(table=table, fk_col_name=fk_col_name))
        cur.execute("alter table {table} add unique ({fk_col_name})""".format(table=table, fk_col_name=fk_col_name))
        cur.execute("alter table {table} add primary key ({fk_col_name})" .format(table=table, fk_col_name=fk_col_name))

def add_foreign_key(table, fk_col_name, foreign_table_name):
    cur.execute("""alter table {table} add foreign key
                    ({fk_col_name}) references {foreign_table_name}""".format(table=table, fk_col_name=fk_col_name,
                                                                               foreign_table_name=foreign_table_name))


def recreate_index(cur, table, idx_name, idx_cols):
    cur.execute('drop index if exists {idx_name}'.format(idx_name=idx_name))
    cur.execute("""create index {idx_name}
                     on {table} ({idx_cols})""".format(table=table,
                                                       idx_name=idx_name,
                                                       idx_cols=idx_cols))


def analyze_table(cur, table):
    cur.execute('vacuum %s' % table)
    cur.execute('analyze %s' % table)


def fix_user_table_pre(conn, cur, tables):
    #cur.execute('alter table core_user add column username_x varchar(50)')
    #cur.execute('update core_user set username_x = username')
    cur.execute('CREATE SEQUENCE user_id_temp_seq')
    cur.execute("alter table core_user add column user_id integer default nextval('user_id_temp_seq')")
    cur.execute('alter table core_user add constraint user_id_unique unique (user_id)')
    cur.execute('alter table crm_appointment drop constraint appointment_user_completed_fkey')
    cur.execute('alter table crm_appointment drop constraint appointment_user_created_fkey')
    cur.execute('alter table cms_content drop constraint cms_content_user_created_fkey')
    cur.execute('alter table cms_page drop constraint cms_page_user_created_fkey')
    cur.execute('alter table cms_site drop constraint cms_site_user_created_fkey')
    cur.execute('alter table crm_appointment drop constraint crm_appointment_user_assigned_fkey')
    cur.execute('alter table crm_billing drop constraint crm_billing_user_created_fkey')
    cur.execute('alter table crm_communication drop constraint crm_communication_user_created_fkey')
    cur.execute('alter table crm_journal drop constraint crm_journal_user_created_fkey')
    cur.execute('alter table crm_product_inventory_journal drop constraint crm_product_inventory_journal_user_created_fkey')
    cur.execute('alter table crm_product_return drop constraint crm_product_return_user_created_fkey')
    cur.execute('alter table crm_customer_order drop constraint customer_order_user_created_fkey')
    cur.execute('alter table crm_customer drop constraint customer_user_assigned_fkey')
    cur.execute('alter table crm_customer drop constraint customer_user_created_fkey')
    cur.execute('alter table crm_order_item drop constraint order_item_user_created_fkey')
    cur.execute('alter table core_status drop constraint status_username_fkey')
    if 'wm_ireport' in tables:
        cur.execute('alter table wm_ireport drop constraint wm_ireport_user_created_fkey')
    cur.execute('alter table core_user drop constraint users_pkey')
    cur.execute('alter table core_user add primary key (user_id)')
    cur.execute("select user_id, username from core_user")
    users = cur.fetchall()
    for usr in users:
        userid = usr[0]
        username = usr[1]
        cur.execute("update crm_appointment set user_completed = '%s' where user_completed = '%s'" % (userid, username))
        cur.execute("update crm_appointment set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update cms_content set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update cms_page set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update cms_site set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update crm_appointment set user_assigned = '%s' where user_assigned = '%s'" % (userid, username))
        cur.execute("update crm_billing set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update crm_communication set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update crm_journal set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update crm_product_inventory_journal set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update crm_product_return set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update crm_customer_order set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update crm_customer set user_assigned = '%s' where user_assigned = '%s'" % (userid, username))
        cur.execute("update crm_customer set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update crm_order_item set user_created = '%s' where user_created = '%s'" % (userid, username))
        cur.execute("update core_status set username = '%s' where username = '%s'" % (userid, username))
        if 'wm_ireport' in tables:
            cur.execute("update wm_ireport set user_created = '%s' where user_created = '%s'" % (userid, username))

    conn.commit()
    cur.execute('alter table crm_appointment alter column user_completed set data type integer using cast (user_completed as integer)')
    cur.execute('alter table crm_appointment alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table cms_content alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table cms_page alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table cms_site alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table crm_appointment alter column user_assigned set data type integer using cast (user_assigned as integer)')
    cur.execute('alter table crm_billing alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table crm_communication alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table crm_journal alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table crm_product_inventory_journal alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table crm_product_return alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table crm_customer_order alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table crm_customer alter column user_assigned set data type integer using cast (user_assigned as integer)')
    cur.execute('alter table crm_customer alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table crm_order_item alter column user_created set data type integer using cast (user_created as integer)')
    cur.execute('alter table core_status alter column username set data type integer using cast (username as integer)')
    if 'wm_ireport' in tables:
        cur.execute('alter table wm_ireport alter column user_created set data type integer using cast (user_created as integer)')
    conn.commit()

    cur.execute('alter table crm_appointment add foreign key (user_completed) REFERENCES core_user')
    cur.execute('alter table crm_appointment add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table cms_content add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table cms_page add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table cms_site add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table crm_appointment add foreign key (user_assigned) REFERENCES core_user')
    cur.execute('alter table crm_billing add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table crm_communication add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table crm_journal add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table crm_product_inventory_journal add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table crm_product_return add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table crm_customer_order add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table crm_customer add foreign key (user_assigned) REFERENCES core_user')
    cur.execute('alter table crm_customer add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table crm_order_item add foreign key (user_created) REFERENCES core_user')
    cur.execute('alter table core_status add foreign key (username) REFERENCES core_user')
    if 'wm_ireport' in tables:
        cur.execute('alter table wm_ireport add foreign key (user_created) REFERENCES core_user')
    conn.commit()
    
def fix_fk_type_table(conn, cur, table):
    cur.execute("alter table {table} add column fk_id_uuid uuid".format(table=table))

    fk_types = [
        ('Asset', 'core_asset', 'id'),
        ('Campaign', 'crm_campaign', 'campaign_id'),
        ('Communication', 'crm_communication', 'comm_id'),
        ('Company', 'crm_company', 'company_id'),
        ('Customer', 'crm_customer', 'customer_id'),
        ('CustomerOrder', 'crm_customer_order', 'order_id'),
        ('Enterprise', 'crm_enterprise', 'enterprise_id'),
        ('Listing', 'pvs_listing', 'listing_id'),
        ('OrderItem', 'crm_order_item', 'order_item_id'),
        ('Product', 'crm_product', 'product_id'),
        ('PurchaseOrder', 'crm_purchase_order', 'purchase_order_id')]

    for fk_type in fk_types:
        typ = fk_type[0]
        far_table = fk_type[1]
        far_col = fk_type[2]
        print 'fix_fk_type_table %s : %s' % (table, typ)

        cur.execute("select count(0) from {table} where fk_type = '{typ}'".format(table=table, typ=typ))
        cnt = cur.fetchone()
        if cnt[0] > 0:
            cur.execute("""update {table} set fk_id_uuid
                           = (select {far_col}_uuid from {far_table} where {far_col} = fk_id) where fk_type = '{typ}'""".format(table=table,
                                                                                                                                far_col=far_col,
                                                                                                                                far_table=far_table,
                                                                                                                                typ=typ))
    cur.execute("alter table {table} drop column fk_id".format(table=table))
    cur.execute("alter table {table} rename column fk_id_uuid to fk_id".format(table=table))
    conn.commit()


def fix_content(conn, cur):
    cur.execute('truncate table cms_content')
    cur.execute('alter table cms_content drop column page_id')
    cur.execute('alter table cms_content drop column is_dynamic')
    cur.execute('alter table cms_content add column site_id integer')
    cur.execute('alter table cms_content add foreign key (site_id) references cms_site')
    conn.commit()


def fix_assets_a(conn, cur, dbname, storage_root):
    cur.execute("alter table core_asset add column extension varchar(10)")
    cur.execute("alter table core_asset add column enterprise_id uuid")
    cur.execute("alter table core_asset add foreign key (enterprise_id) references crm_enterprise")
    conn.commit()

def fix_assets_b(conn, cur, dbname, storage_root):
    # there's only one enterprise at a time, so this works.
    cur.execute("select enterprise_id from crm_enterprise limit 1")
    default_enterprise_id = cur.fetchone()[0]

    enterprises = []
    assets = []
    with open('%s-keys.log' % dbname, 'r') as keylog:
        for lin in keylog.readlines():
            parts = lin.split(':')
            if parts[0] == 'crm_enterprise':
                enterprises.append(parts[1:])
            elif parts[0] == 'core_asset':
                assets.append(parts[1:])
        
    for ass in assets:
        cur.execute("select id, fk_type, fk_id, name, web_path from core_asset where id = '%s'" % ass[1][:-1]) #chop line feed
        assid, fk_type, fk_id, name, web_path = cur.fetchone()
        enterprise_id = ext = basename = None
        if 'Listing' == fk_type:
            if not fk_id:
                print "** Listing no fk_id for %s (%s)" % (ass[1][:-1], web_path)
                continue
            cur.execute("""select l.listing_id, l.company_id, c.enterprise_id
                            from pvs_listing l, crm_company c
                            where l.company_id = c.company_id and l.listing_id = '%s'""" % fk_id)
            listing_id, company_id, enterprise_id = cur.fetchone()
            basename = os.path.basename(web_path)
            ext = os.path.splitext(web_path)[1]
        elif 'Product' == fk_type:
            if not fk_id:
                print "** Product no fk_id for %s (%s)" % (ass[1][:-1], web_path)
                continue
            cur.execute("""select p.product_id, p.company_id, c.enterprise_id
                            from crm_product p, crm_company c
                            where p.company_id = c.company_id and p.product_id = '%s'""" % fk_id)
            product_id, company_id, enterprise_id = cur.fetchone()
        enterprise_id = util.nvl(enterprise_id, default_enterprise_id)
        basename = os.path.basename(web_path)
        ext = os.path.splitext(web_path)[1]
        cmd = "mkdir -p {storage_root}/enterprises/{enterprise_id}/assets/{_0}/{_1}/{_2}".format(storage_root=storage_root,
                                                                                                 enterprise_id=enterprise_id,
                                                                                                 _0=assid[0],
                                                                                                 _1=assid[1],
                                                                                                 _2=assid[2])
        util.run_process(cmd.split(' '))
        if os.path.exists("{storage_root}{web_path}".format(storage_root=storage_root, web_path=web_path)):
            src = "{storage_root}{web_path}".format(storage_root=storage_root,
                                                    web_path=web_path)
            dst = "{storage_root}/enterprises/{enterprise_id}/assets/{_0}/{_1}/{_2}/{assid}{ext}".format(storage_root=storage_root,
                                                                                                          enterprise_id=enterprise_id,
                                                                                                          _0=assid[0],
                                                                                                          _1=assid[1],
                                                                                                          _2=assid[2],
                                                                                                          assid=assid,
                                                                                                          ext=ext)
            shutil.copyfile(src, dst)
            if os.path.exists("{storage_root}/enterprises/{enterprise_id}/assets/{_0}/{_1}/{_2}/{assid}{ext}".format(storage_root=storage_root,
                                                                                                                         enterprise_id=enterprise_id,
                                                                                                                         _0=assid[0],
                                                                                                                         _1=assid[1],
                                                                                                                         _2=assid[2],
                                                                                                                         assid=assid,
                                                                                                                         ext=ext)):

                cur.execute("update core_asset set enterprise_id = '{ent_id}', extension = '{ext}' where id = '{id}'".format(ent_id=enterprise_id,
                                                                                                                             ext=ext,
                                                                                                                             id=assid))
            else:
                print "Bogus enterprise asset %s %s" % (assid, web_path)
        else:
            print "Bogus company asset %s" % web_path

        #    cur.execute("select 
        #    print 'cp %s 
    conn.commit()
        
def fix_date(conn, cur):
    for table_name, column_name, data_type in get_columns_of_type(cur, 'date'):
        change_type(cur, table_name, column_name, 'timestamp')
        

# def dump_asset_keys(cur, dbname):
#     with open("%s-filesystem-keys.log" % dbname, "w") as f:
#         cur.execute("select site_id from cms_site")
#         for site_id in [site_[0] for site_ in cur.fetchall()]:
#             f.write("cms_site:%s:%s" % (site_id, md5(str(site_id)).hexdigest()))
#    
#         cur.execute("select company_id, customer_id, listing_id from pvs_listing")
#         for listing in cur.fetchall():
#             salt = 'derf'
#             #md5('%s%s%s%s' % (self.company_id, self.customer_id, self.listing_id, salt)).hexdigest()
#             f.write("pvs_listing:%s:%s:%s:%s" % (listing[0], listing[1], listing[2], md5('%s%s%s%s' % (listing[0], listing[1], listing[2], salt)).hexdigest()))
#    
#         cur.execute("select company_id from crm_company")
#         for company_id in [comp[0] for comp in cur.fetchall()]:
#             f.write("crm_company:%s:%s" % (str(company_id), md5(str(company_id)).hexdigest()))
#
#         cur.execute("select id, name, fk_type, fk_id from core_asset")
#         for asset_id, filename, fk_type, fk_id in cur.fetchall():
#             import pdb; pdb.set_trace()
#             if "Listing" == fk_type:
#                 filename = md5('%s%s' % (filename, fk_id)).hexdigest()
#                 folder = 'images/%s/%s/%s' % (filename[0], filename[1], filename[2])
#                 extension = os.path.splitext(filename)[1]
#                 fs_path = os.path.join(folder, filename+extension)
#                 fs_path_real = os.path.join('%s/%s' % (site.site_full_directory, folder), filename+extension)
#             elif 'Product' == fk_type:
#                 pass


if __name__ == '__main__':
    dbname = sys.argv[1]
    conn = psycopg2.connect("dbname=%s user=%s password=%s host=localhost" % (sys.argv[1], sys.argv[1], sys.argv[2]))
    cur = conn.cursor()
    storage_root = sys.argv[3]

    tables = list_tables(cur)

    fix_user_table_pre(conn, cur, tables)
    fix_date(conn, cur)
    fix_content(conn, cur)

    conn.commit()

    # go get the primary keys, foreign keys, and indexes so we can remember them
    # later after we drop them.  Make sure they are integer keys.
    primary_keys = {}
    foreign_keys = {}
    indexes = {}
    for table in tables:
        print "\n\n\nremembering keys for %s" % table
        pkeys = list_keys(cur, table, 'PRIMARY')
        if pkeys and len(pkeys):
            pkey = pkeys[0]
            pk_col_name = pkey[2]
            if 'integer' != get_column_type(cur, table, pk_col_name):
                continue
            primary_keys[table] = pkey
            foreign_keys[table] = []
            fkeys = list_keys(cur, table, 'FOREIGN')
            for fkey in fkeys:
                fk_col_name = fkey[2]
                if 'integer' != get_column_type(cur, table, fk_col_name):
                    continue
                foreign_keys[table].append(fkey)
            indexes[table] = get_indexes(cur, table)

    # Go create PK mirror columns for every table where the PK is an
    # autoincrement integer.
    for table in tables:
        if not table in primary_keys:
            continue
        print "\n\n\ncreating uuid primary key col for %s" % table
        pkey = primary_keys[table]
        pk_col_name = pkey[2]
        add_uuid_col(cur, table, pk_col_name)
        pk_vals = get_pk_vals(cur, table, pk_col_name)
        for i, pk_val in enumerate(pk_vals):
            update_uuid_for_pk(cur, table, pk_col_name, pk_val)
            conn.commit()
            if (i % 1000) == 0:
                print "    %s %s/%s" % (table, i+1, len(pk_vals))

    # Go create mirror foreign key columns for each table where the
    # foreign PK is an autoincrement integer
    for table in tables:
        if not table in primary_keys:
            continue
        print "\n\n\nfilling in foreign keys for %s" % table
        pkey = primary_keys[table]
        pk_col_name = pkey[2]
        pk_vals = get_pk_vals(cur, table, pk_col_name)
        fkeys = foreign_keys[table]
        for fkey in fkeys:
            fk_constraint_name = fkey[0]
            fk_col_name = fkey[2]
            foreign_table_name = fkey[3]
            foreign_column_name = fkey[4]
            add_uuid_col(cur, table, fk_col_name)
            conn.commit()
            for i, pk_val in enumerate(pk_vals):
                set_foreign_uuid_val(cur, table, pk_col_name, pk_val, fk_col_name, foreign_table_name, foreign_column_name)
                conn.commit()
                if (i % 1000) == 0:
                    print "    %s %s/%s" % (table, i+1, len(pk_vals))

    # go drop the foreign key and primary key constraints on every
    # table.  It's ok to do this because we saved the current
    # configuration in primary_keys and foreign_keys.  We'll reconstruct
    # everything later.                    
    for table in tables:
        if not table in primary_keys:
            continue
        print "\n\n\ndropping constraints %s" % table
        pkey = primary_keys[table]
        pk_constraint_name = pkey[0]
        drop_constraint(cur, table, pk_constraint_name)
        conn.commit()
        fkeys = foreign_keys[table]
        for fkey in fkeys:
            fk_constraint_name = fkey[0]
            drop_constraint(cur, table, fk_constraint_name)
            conn.commit()

    # fix fk_type/fk_id faux foreign key references.
    fix_fk_type_table(conn, cur, 'core_attribute_value')
    fix_fk_type_table(conn, cur, 'core_status')
    fix_fk_type_table(conn, cur, 'core_asset')
    fix_fk_type_table(conn, cur, 'core_key_value')
    
    # dump all the table_name : integer key -> uuid key
    with open('%s-keys.log' % sys.argv[1], 'w') as f:
        for table in tables:
            if not table in primary_keys:
                continue
            print "\n\n\ndumping keys on %s" % table
            pkey = primary_keys[table]
            pk_col_name = pkey[2]
            pk_vals = get_old_and_new_pk_vals(cur, table, pk_col_name)
            for i, pk_val in enumerate(pk_vals):
                f.write('%s:%s:%s\n' % (table, pk_val[0], pk_val[1]))
                if (i % 1000) == 0:
                    print "    %s %s/%s" % (table, i+1, len(pk_vals))
                    
    # drop integer columns and rename the *_uuid colums to the name of
    # the old pk columns
    for table in tables:
        if not table in primary_keys:
            continue
        print "\n\n\nrenaming columns on %s" % table
        pkey = primary_keys[table]
        pk_col_name = pkey[2]
        rename_uuid_col(cur, table, pk_col_name, True)
        conn.commit()
        fkeys = foreign_keys[table]
        for fkey in fkeys:
            fk_col_name = fkey[2]
            rename_uuid_col(cur, table, fk_col_name)
            conn.commit()

    # reinstate the old foreign keys
    for table in tables:
        if not table in primary_keys:
            continue
        print "\n\n\nreinstating foreign keys for %s" % table
        fkeys = foreign_keys[table]
        for fkey in fkeys:
            fk_col_name = fkey[2]
            foreign_table_name = fkey[3]
            add_foreign_key(table, fk_col_name, foreign_table_name)
            conn.commit()
        

    # make sure all the non-pk indexes are still there.
    for table in [table for table in indexes if len(indexes[table]) > 0]:
        for idx in indexes[table]:
            idx_name = idx[1]
            idx_cols = idx[2]
            recreate_index(cur, table, idx_name, idx_cols)
            conn.commit()
                        
    conn.set_isolation_level(0)
    # analyze and vacuum tables
    for table in tables:
        if not table in primary_keys:
            continue
        print "\n\n\nvacuuming for %s" % table
        analyze_table(cur, table)

    conn.commit()
    fix_assets_a(conn, cur, dbname, storage_root)
    fix_assets_b(conn, cur, dbname, storage_root)

    conn.commit()
    cur.close()
    conn.close()




    
    
