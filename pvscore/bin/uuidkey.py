# import psycopg2
# import sys


# def list_tables(cur):
#     cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
#     return cur.fetchall()


# def list_foreign_keys(cur, tablename):
#     cur.execute("""
#         SELECT
#             tc.constraint_name, tc.table_name, kcu.column_name, 
#             ccu.table_name AS foreign_table_name,
#             ccu.column_name AS foreign_column_name 
#         FROM 
#             information_schema.table_constraints AS tc 
#             JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
#             JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
#         WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='%s'""" % tablename)
#     return cur.fetchall()


# if __name__ == '__main__':
#     conn = psycopg2.connect("dbname=%s user=%s password=%s host=localhost" % (sys.argv[1], sys.argv[1], sys.argv[2]))
#     cur = conn.cursor()

#     tables = list_tables(cur)

#     for table in tables:
#         fks = list_foreign_keys(cur, table
#         print t


#     # Close communication with the database
#     cur.close()
#     conn.close()




    
