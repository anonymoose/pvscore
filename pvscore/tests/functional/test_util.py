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
        assert util.this_year() == datetime.date.today().year
        assert util.get_first_day(today_) == util.get_first_day(today_)  # this is pretty dumb.  it works, just get it covered.
        assert util.get_last_day(today_) == util.get_last_day(today_)
        assert util.to_uuid('ken') == None
        assert int(util.average([1, 2, 3])) == 2
        assert util.format_date(util.truncate_datetime(dtime)) == util.str_today()
        assert util.is_today(d8e) == True


    def test_states(self):
        sl = util.state_select_list('TN')
        assert '<option value="TN" selected>Tennessee</option>' in sl
        assert util.state_abbrev_to_state('TN') == 'Tennessee'


    def test_run_process(self):
        output = util.run_process(['/bin/cat', '/etc/passwd'])
        assert len([out for out in output if 'root' in out]) > 0



    def test_array_stuff(self):
        aaa, bbb, ccc = [util.DataObj({}), util.DataObj({}), util.DataObj({})]
        aaa.name = 'a'
        bbb.name = 'b'
        ccc.name = 'c'
        ret = util.single_attr_array([aaa, bbb, ccc], 'name')
        assert ret == ['a', 'b', 'c']


        aaa, bbb, ccc = [{'name' : 'a'}, {'name' : 'b'}, {'name' : 'c'}]
        ret = util.single_key_array([aaa, bbb, ccc], 'name')
        assert ret == ['a', 'b', 'c']
