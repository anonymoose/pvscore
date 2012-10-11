#pylint: disable-msg=W0612,C0103,R0903
import pvscore.lib.db as db
from pvscore.tests import TestController

# bin/T pvscore.tests.functional.test_db

class TestDb(TestController):

    def test_commit(self):
        db.execute("drop table if exists testtable")
        db.execute("create table testtable ( x int not null )")
        db.execute("insert into testtable (x) values (123)")
        db.commit()
        v = db.get_value("select x from testtable")
        assert v == 123
        db.execute("drop table testtable")


    def test_get_result_set(self):
        custs = db.get_result_set(['customer_id', 'fname', 'lname'],
                                  "select customer_id, fname, lname from crm_customer where lname = 'Bedwell'")
        assert len(custs) > 0
        assert custs[0].lname == 'Bedwell'
