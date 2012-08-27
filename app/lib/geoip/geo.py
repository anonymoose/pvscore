import pygeoip

""" KB: [2011-03-28]: 
http://code.google.com/p/pygeoip/wiki/Usage
"""
class Geo:
    def __init__(self):
        self.gic = None
        try:
            path = config['app_conf']['pvs.geoip.dat.file.path']
            if path:
                self.gic = pygeoip.GeoIP(path)
        except:
            pass
        
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

    def by_ip(self, ip):
        if ip == '127.0.0.1': ip = '98.231.77.218' # only happens in dev
        if self.gic:
            return self.gic.record_by_addr(ip)

