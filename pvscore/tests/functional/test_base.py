from unittest import TestCase
from pvscore.controllers.base import BaseController
from pyramid.httpexceptions import HTTPForbidden
import logging

log = logging.getLogger(__name__)

# bin/T pvscore.tests.functional.test_base

class TestBase(TestCase):
    def test_forbid_if(self):
        tst = TestController(None)
        excepted = False
        try:
            tst.it_is_forbidden()
            self.assertEqual(True, False)
        except HTTPForbidden as forbidden:
            log.info(forbidden)
            excepted = True
        self.assertEqual(excepted, True)



class TestController(BaseController):
    def it_is_forbidden(self):
        self.forbid_if(True, "this is message")
