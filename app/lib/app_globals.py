"""The application's Globals object"""


from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
#from turbomail.adapters import tm_pylons

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self, config):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.cache = CacheManager(**parse_cache_config_options(config))

        """ KB: [2010-10-21]: Turbomail setup """
#        tm_pylons.config = config
#        tm_pylons.start_extension()


