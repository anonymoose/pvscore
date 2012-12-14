#pylint: disable-msg=W0612,C0103,R0903
import pvscore.lib.helpers as h
import pvscore.lib.util as util
from pvscore.tests import TestController
from pyramid import testing
import datetime

# bin/T pvscore.tests.functional.test_helpers

class TestHelpers(TestController):
    def test_google_analytics(self):
        val = h.google_analytics(self.site)
        self.assertEqual(val is not None, True)
        val = h.eyefoundit_analytics(self.site)
        self.assertEqual(val is not None, True)


    def test_dates(self):
        d8e = util.today_date()
        dtime = util.today()
        assert h.is_today(d8e)
        assert h.str_today() == util.str_today()
        assert h.date_time(None) == ''
        assert h.date_time(d8e) == d8e.strftime("%Y-%m-%d %H:%M:%S")
        assert h.date_(None) == ''
        assert h.date_(d8e) == d8e.strftime("%Y-%m-%d")
        assert h.format_date(None) == ''
        assert h.format_date(d8e) == d8e.strftime("%Y-%m-%d")
        assert h.words_date_time(None) == ''
        assert h.words_date_time(dtime) == dtime.strftime("%B %d, %Y at %I:%M %p")
        assert h.slash_date(None) == ''
        assert h.slash_date(dtime) == dtime.strftime("%m/%d/%Y")
        assert h.words_date(None) == ''
        assert h.words_date(dtime) == dtime.strftime("%B %d, %Y")
        assert h.this_year() == datetime.date.today().year
        self.assertEqual('checkbox' in h.chkbox('fud'), True)

        dobj = TestObj()
        assert h.get(dobj, 'a') == 'aa'
        assert h.get(dobj, 'bogus') == ''

    def test_is_api(self):
        assert h.is_api(testing.DummyRequest()) == False


    def test_unique_links(self):
        assert h.nl2br('\n\n\n') == '<br>\n<br>\n<br>\n'
        req = testing.DummyRequest()
        assert '?rnd' in h.javascript_link_ex('fuz', req)
        assert 'fuz'  in h.javascript_link_ex('fuz', req)
        assert '?rnd' in h.stylesheet_link_ex('fuz', req)
        assert 'fuz'  in h.stylesheet_link_ex('fuz', req)

    def test_misc(self):
        dobj = TestObj()
        assert h.onvl(dobj, 'a', '_default_') == 'aa'
        assert h.onvl(dobj, 'x', '_default_') == '_default_'
        assert h.onvl(None, 'x', '_default_') == '_default_'
        assert h.is_production() == False
        assert '<option value="TN" selected>Tennessee</option>' in h.state_select_list('TN')

class TestObj(object):
    def __init__(self):
        self.a = 'aa'
        self.b = 'bb'
