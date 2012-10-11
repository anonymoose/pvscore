#pylint: disable-msg=W0612,C0103,R0903
import pvscore.lib.helpers as h
import pvscore.lib.util as util
from pvscore.tests import TestController
from pyramid import testing

# bin/T pvscore.tests.functional.test_util

class TestUtil(TestController):
    def test_util(self):
        d8e = util.today_date()
        dtime = util.today()
        assert util.format_rss_date(d8e) == d8e.strftime("%a, %d %b %Y %H:%M:%S EST")
        assert util.words_date(dtime) == dtime.strftime("%B %d, %Y")
        assert util.is_empty(' ') == True
        assert util.float_('8') == None
        assert util.page_list([1, 2, 3, 4, 5, 6, 7, 8, 9], 2, 2) == [3, 4]
        assert util.page_list([1, 2, 3, 4, 5, 6, 7, 8, 9], None, None) == [1, 2, 3, 4, 5, 6, 7, 8, 9]



