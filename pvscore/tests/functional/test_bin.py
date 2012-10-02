from unittest import TestCase
from pvscore.bin import pyramid_script, log
import sys, os


# bin/T pvscore.tests.functional.test_bin

class TestBin(TestCase):
    def test_no_ini(self):
        os.environ['is_debug'] = 'True'
        try:
            pyramid_script_t()
            self.assertEqual(True, False)
        except Warning as war:
            log(war)
        finally:
            del os.environ['is_debug']


    def test_with_ini(self):
        sys.argv.append("-I")
        sys.argv.append("unittest.ini")
        pyramid_script_t()
        del sys.argv[-2:]

    def test_barf_no_debug(self):
        sys.argv.append("-I")
        sys.argv.append("unittest.ini")
        try:
            pyramid_barf_script()
        except Exception as exc:
            log(exc)
            self.assertEqual(True, False)
        finally:
            del sys.argv[-2:]

    def test_barf_debug(self):
        sys.argv.append("-I")
        sys.argv.append("unittest.ini")
        os.environ['is_debug'] = 'True'
        try:
            pyramid_barf_script()
            self.assertEqual(True, False)
        except Exception as exc:
            log(exc)
        finally:
            del os.environ['is_debug']
            del sys.argv[-2:]


@pyramid_script
def pyramid_script_t():
    return True


@pyramid_script
def pyramid_barf_script():
    raise Exception("This barfed")

