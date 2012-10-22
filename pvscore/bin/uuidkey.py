import psycopg2
import sys
import uuid
from pprint import pprint

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
    cur.execute('vacuum %s' % table);
    cur.execute('analyze %s' % table);


#
# T = table list
# for all t in T
#     PK = primary key (t)
#     if len(PK) == 1 and PK.type == integer
#         pk = PK[0]
#         alter table $t.table_name add column $pk.column_name+uuid uuid not null;
#         ROWS = select $pk.column_name from $t.table_name
#         for all row in ROWS:
#             update $t.table_name set $pk.column_name+uuid = uuid.uuid4()
#
# for all t in T
#     FK = foreign keys (t)
#     for all fk in FK
#         
#         alter table $t.table_name drop $fk.constraint_name
#
#
#
if __name__ == '__main__':
    conn = psycopg2.connect("dbname=%s user=%s password=%s host=localhost" % (sys.argv[1], sys.argv[1], sys.argv[2]))
    cur = conn.cursor()

    tables = list_tables(cur)

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
        print "\n\n\ndropping constraintsing %s" % table
        pkey = primary_keys[table]
        pk_constraint_name = pkey[0]
        drop_constraint(cur, table, pk_constraint_name)
        conn.commit()
        fkeys = foreign_keys[table]
        for fkey in fkeys:
            fk_constraint_name = fkey[0]
            drop_constraint(cur, table, fk_constraint_name)
            conn.commit()

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

    cur.close()
    conn.close()




    
    
