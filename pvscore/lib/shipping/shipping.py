import logging
import pvscore.lib.util as util
import simplejson as json
from pyramid.renderers import render
import urllib2
try:
    from xml.etree.ElementTree import fromstring, tostring
except ImportError:
    from elementtree.ElementTree import fromstring, tostring

log = logging.getLogger(__name__)

class UPSShipping(object):
    def __init__(self):
        self.raw = None


    def _process_request(self, connection, request):
        """
        Post the data and return the XML response
        """
        conn = urllib2.Request(url=connection, data=request.encode("utf-8"))
        f = urllib2.urlopen(conn)
        all_results = f.read()
        self.raw = all_results
        return fromstring(all_results)


    def get_options(self, customer, site, cart):
        site_config = json.loads(site.config_json) if site.config_json else None
        if not site_config:
            raise Exception("No site config for UPS Shipping.")
        
        shipping_config = site_config[0]['shipping']
        xml = util.literal(render('/catalog/shipping.ups_pricing_call.mako',
                                  {'cust' : customer,
                                   'campaign' : customer.campaign,
                                   'company' : customer.campaign.company,
                                   'api_key' : shipping_config['api_key'],
                                   'user_id' : shipping_config['user_id'],
                                   'account' : shipping_config['account'],
                                   'password' : shipping_config['password'],
                                   'container' : shipping_config['container_choices_default'],
                                   'pickup' : shipping_config['pickup_type_choices_default'],
                                   'total_weight' : sum([util.nvl(item['product'].weight, '1') for item in cart.items]),
                                   'cart' : cart,
                                   'site' : site
                                   }))

        tree = self._process_request(shipping_config['ups_url'], xml)
        try:
            status_code = tree.getiterator('ResponseStatusCode')
            status_val = status_code[0].text
        except AttributeError:
            status_val = "-1"

        options = []
        charges = delivery_days = None
        if status_val == '1':
            all_rates = tree.getiterator('RatedShipment')
            for response in all_rates:
                charges = response.find('.//TotalCharges/MonetaryValue').text
                if response.find('.//GuaranteedDaysToDelivery').text:
                    delivery_days = response.find('.//GuaranteedDaysToDelivery').text
                code = response.find('.//Service/Code')
                if code is not None and code.text in shipping_config['timeframe_choices']:
                    option = {}
                    option['code'] = code.text
                    option['name'] = shipping_config['timeframe_choices'][code.text]
                    option['charges'] = charges
                    option['delivery_days'] = util.nvl(delivery_days)
                    options.append(option)
        else:
            try:
                errors = tree.find('.//Error')
                log.error("UPS %s Error: Code %s - %s" % (errors[0].text, errors[1].text, errors[2].text))
            except AttributeError:
                log.error("UPS error - cannot parse response:\n %s" % self.raw)
        return options


