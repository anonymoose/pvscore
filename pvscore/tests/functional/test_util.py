#pylint: disable-msg=W0612,C0103,R0903
import pvscore.lib.util as util
from pvscore.tests import TestController
import datetime

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
        assert util.parse_date('2012-05-06') == datetime.datetime.strptime('2012-05-06', '%Y-%m-%d')
        today_ = datetime.date.today()
        assert [today_.year + 10, today_.year + 10] in util.year_list()
        assert util.month_list()[0] == ["1", "January"]
        

    def test_states(self):
        sl = util.state_select_list('TN')
        assert '<option value="TN" selected>Tennessee</option>' in sl
        assert util.state_abbrev_to_state('TN') == 'Tennessee'


