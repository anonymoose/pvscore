"""Import the TCD_sample_database model into your script"""
import commands, traceback, os, time, pdb
from paste.deploy import appconfig
import getopt, sys
from optparse import OptionParser
import pvscore.lib.util as util
from pyramid.paster import bootstrap
from pvscore import command_line_main
import paste.deploy


def init_pyramid(config_file_path=None):
    if config_file_path == None:
        config_file_path = os.getcwd() + '/prod.ini'
    else:
        config_file_path = os.getcwd() + '/' + config_file_path
    settings = paste.deploy.appconfig('config:%s' % config_file_path, relative_to='.')
    return command_line_main(settings)


# so we only call this once.
_initialized = False


""" KB: [2012-01-04]: http://code.activestate.com/recipes/546512/ """
class SingleInstance(object):
    def __init__(self, pidPath):
        """ KB: [2012-01-04]:
        pidPath - full path/filename where pid for running application is to be
                  stored.  Often this is ./var/<pgmname>.pid
        """
        self.pidPath = pidPath
        if os.path.exists(pidPath):
            # Make sure it is not a "stale" pidFile
            pid = open(pidPath, 'r').read().strip()

            # Check list of running pids, if not running it is stale so
            # overwrite
            pidRunning = commands.getoutput('ls /proc | grep %s' % pid)
            if pidRunning:
                self.lasterror = True
            else:
                self.lasterror = False
        else:
            self.lasterror = False

        if not self.lasterror:
            # Write my pid into pidFile to keep multiple copies of program from running.
            fp = open(pidPath, 'w')
            fp.write(str(os.getpid()))
            fp.close()

    def already_running(self):
        return self.lasterror

    def __del__(self):
        if not self.lasterror:
            os.unlink(self.pidPath)

class PVSOptionParser(OptionParser):
    """ KB: [2011-11-08]: this is to ignore invalid command line arguments so that you can pass -I and it get parsed in init_pyramid
    and pass --foobaz and have it parsed elsewhere.
    """
    def error(self, msg):
        pass

""" KB: [2011-11-08]: This is so OptionParser will work, provided -I /whatever is the first arg """
ARGV = sys.argv[sys.argv.index('-I')+1:] if '-I' in sys.argv else sys.argv

# call scripts like so
#    python -c 'from app.bin.local.wm.stock_data import split_exchange_csv; split_exchange_csv("nasdaq")' -I wm-dev.ini
#
# OR...
#
#    export PYRAMID_INI=wm-dev.ini
#    python -c 'from app.bin.local.wm.stock_data import split_exchange_csv; split_exchange_csv("nasdaq")'
def pyramid_script(func):
    def _init_pyramid(*args, **kwargs):
        single = SingleInstance("/tmp/%s.%s.pid" % (func.__module__, func.__name__))
        try:
            if single.already_running():
                sys.exit("Another instance of this program is already running")

            if not _initialized:
                if 'PYRAMID_INI' in os.environ:
                    inifile = os.environ['PYRAMID_INI']
                else:
                    inifile = None
                    for i,a in enumerate(sys.argv):
                        if a == '-I':
                            inifile = sys.argv[i+1]
                            break
                if not inifile: raise Warning
                init_pyramid(inifile)
            try:
                res = func(*args, **kwargs)
                return res
            except:
                if 'is_debug' in os.environ and os.environ['is_debug'] == 'True':
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    subj = 'BATCH %s %s.%s (%s.%s)' % (util.hostname(), func.__module__, func.__name__, exc_type.__module__, exc_type.__name__)
                    if 'exceptions.KeyboardInterrupt' != subj:
                        log('**** EXCEPTION %s' % subj)
                        msg = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
                        util.quickmail(subj, msg.replace("\\n", "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;").replace("', '  File", 'File').replace("'", ''))
        finally:
            del single

    return _init_pyramid

def log(s):
    try:
        print "%s -- %s" % (time.ctime(), s)
        sys.stdout.flush()
    except: pass

def email(to, subj, msg):
    from pvscore.lib.base import BaseUI
    from pvscore.model.crm.company import Company, Enterprise
    Enterprise.load(BaseUI.get_enterprise_id())
    mail = UserMail(Company.find_all()[0])
    mail.send(to, subj, msg)
