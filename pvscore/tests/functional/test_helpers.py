#pylint: disable-msg=W0612,C0103,R0903
import pvscore.lib.helpers as h
import pvscore.lib.util as util
from pvscore.tests import TestController

# bin/T pvscore.tests.functional.test_helpers

class TestHelpers(TestController):
    def test_google_analytics(self):
        val = h.google_analytics(self.site)
        self.assertEqual(val is not None, True)


    def test_dates(self):
        d8e = util.today_date()
        dtime = util.today()
        self.assertEqual(h.date_time(d8e), d8e.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(h.date_(d8e), d8e.strftime("%Y-%m-%d"))
        self.assertEqual(h.format_date(d8e), d8e.strftime("%Y-%m-%d"))
        self.assertEqual(h.words_date_time(dtime), dtime.strftime("%B %d, %Y at %I:%M %p"))
        self.assertEqual(h.slash_date(dtime), dtime.strftime("%m/%d/%Y"))
        self.assertEqual(h.words_date(dtime), dtime.strftime("%B %d, %Y"))
        self.assertEqual('checkbox' in h.chkbox('fud'), True)        

        dobj = TestObj()
        self.assertEqual(h.get(dobj, 'a'), 'aa')
        self.assertEqual(h.get(dobj, 'bogus'), '')


class TestObj(object):
    def __init__(self):
        self.a = 'aa'
        self.b = 'bb'
