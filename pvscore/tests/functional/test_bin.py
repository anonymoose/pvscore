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


    def test_with_env_ini(self):
        try:
            os.environ['PYRAMID_INI'] = 'unittest.ini'
            pyramid_script_t()
        finally:
            del os.environ['PYRAMID_INI']


    def test_barf_no_debug(self):
        sys.argv.append("-I")
        sys.argv.append("unittest.ini")
        excepted = False
        try:
            pyramid_barf_script()
        except Exception as exc:
            log(exc)
            excepted = True
        finally:
            del sys.argv[-2:]
        self.assertEqual(excepted, False)

    def test_barf_debug(self):
        sys.argv.append("-I")
        sys.argv.append("unittest.ini")
        os.environ['is_debug'] = 'True'
        excepted = False
        try:
            pyramid_barf_script()
        except Exception as exc:
            log(exc)
            excepted = True
        finally:
            del os.environ['is_debug']
            del sys.argv[-2:]
        self.assertEqual(excepted, True)


    def test_run_twice(self):
        sys.argv.append("-I")
        sys.argv.append("unittest.ini")
        os.environ['is_debug'] = 'True'
        excepted = False
        try:
            pyramid_run_twice()
        except Exception as exc:
            excepted = True
            log(exc)
        finally:
            del os.environ['is_debug']
            del sys.argv[-2:]
        self.assertEqual(excepted, True)


@pyramid_script
def pyramid_script_t():
    return True


@pyramid_script
def pyramid_barf_script():
    raise Exception("This barfed")


@pyramid_script
def pyramid_run_twice():
    pyramid_run_twice()

