from pvscore.tests import TestController, secure
import logging

log = logging.getLogger(__name__)


class TestValidate(TestController):
    
    def test_invalid_login(self):
        #KB: [2011-09-02]: Everything is valid except that we are not logged in. Should redirect
        barfed = False
        try:
            self.get('/tsst/tsst_validate', {'fname':'ken',
                                             'email':'kenneth.bedwell@gmail.com',
                                             'password':'sWordfish',
                                             'confirm':'bogus'})
        except Exception as exc:
            log.info(exc)
            barfed = True
        assert barfed


    @secure
    def test_simple_success_validate(self):
        R = self.get('/tsst/tsst_validate', {'fname':'ken',
                                             'email':'kenneth.bedwell@gmail.com',
                                             'password':'sWordfish',
                                             'confirm':'sWordfish'})
        assert R.status_int == 200
        assert R.body == 'CALLED:tsst_validate'


    @secure
    def test_redirto(self):
        assert self.get('/tsst/tsst_redirto', {'a':'1.1'}).body == 'CALLED:tsst_redirto'
        assert self.get('/tsst/tsst_redirto', {'a':'x'}).body == 'REDIRECTED_TO OK'


    @secure
    def test_float(self):
        assert self.get('/tsst/tsst_float', {'a':'1.1'}).body == 'CALLED:tsst_float'
        assert self.get('/tsst/tsst_float', {'a':'1'}).body == 'CALLED:tsst_float'
        excepted = False
        try:
            self.get('/tsst/tsst_float', {'a':'ken'})
        except Exception as exc:
            log.info(exc)
            excepted = True
        assert excepted


    @secure
    def test_int(self):
        assert self.get('/tsst/tsst_int', {'a':'1'}).body == 'CALLED:tsst_int'
        excepted = False
        try:
            self.get('/tsst/tsst_int', {'a':'1.1'})
        except Exception as exc:
            log.info(exc)
            excepted = True
        assert excepted
        excepted = False

        try:
            self.get('/tsst/tsst_int', {'a':'ken'})
        except Exception as exc:
            log.info(exc)
            excepted = True
        assert excepted


    @secure
    def test_string(self):
        assert self.get('/tsst/tsst_string', {'a':'test'}).body == 'CALLED:tsst_string'
        excepted = False
        try:
            self.get('/tsst/tsst_string', {'a':'1'})
        except Exception as exc:
            log.info(exc)
            excepted = True
        assert excepted
        excepted = False
        self.get('/tsst/tsst_string', {'a':'ken'})


    @secure
    def test_number(self):
        assert self.get('/tsst/tsst_number', {'a':'1.1'}).body == 'CALLED:tsst_number'
        assert self.get('/tsst/tsst_number', {'a':'1'}).body == 'CALLED:tsst_number'
        excepted = False
        try:
            self.get('/tsst/tsst_number', {'a':'ken'})
        except Exception as exc:
            log.info(exc)
            excepted = True
        assert excepted


    @secure
    def test_equals(self):
        assert self.get('/tsst/tsst_equals', {'b':'11'}).body == 'CALLED:tsst_equals'
        assert self.get('/tsst/tsst_equals', {'a': 'ken', 'b':'ken'}).body == 'CALLED:tsst_equals'

        err = False
        try:
            self.get('/tsst/tsst_equals', {'a':'1.1'})
        except Exception as exc:
            log.info(exc)
            err = True
        assert err
        err = False
        try:
            self.get('/tsst/tsst_equals', {'a':'1.1', 'b':'11'})
        except Exception as exc:
            log.info(exc)
            err = True
        assert err



        

