import pygeoip
import logging
import os
import pvscore.lib.util as util

log = logging.getLogger(__name__)

class Geo:
    """ KB: [2011-03-28]:
    http://code.google.com/p/pygeoip/wiki/Usage
    """
    def __init__(self):
        self.gic = None
        try:
            path = '%s/%s' % (os.path.dirname(__file__), 'GeoLiteCity.dat')
            if path:
                self.gic = pygeoip.GeoIP(path)
        except Exception as exc: #pragma: no cover
            log.debug(exc)


    def by_request(self, req):
        """ KB: [2011-03-28]:
        {'city'         : 'Mountain View',
         'region_name'   : 'CA',
         'area_code'     : 650,
         'longitude'     : -122.0574,
         'latitude'      : 37.419199999999989,
         'country_code3' : 'USA',
         'postal_code'   : '94043',
         'dma_code'      : 807,
         'country_code'  : 'US',
         'country_name'  : 'United States'}
        """
        return self.by_ip(req.remote_addr)


    def by_ip(self, ipaddr):
        if ipaddr == '127.0.0.1':
            ipaddr = '98.231.77.218' #pragma: no cover
        if self.gic:
            return self.gic.record_by_addr(ipaddr)

