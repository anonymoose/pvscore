import logging
import pvscore.lib.util as util
import simplejson as json
from pyramid.renderers import render
import urllib2
try:
    from xml.etree.ElementTree import fromstring#, tostring
except ImportError:  #pragma: no cover
    from elementtree.ElementTree import fromstring #pylint: disable-msg=F0401

log = logging.getLogger(__name__)

# class USPSShipping(object):
#     def get_options(self, customer, site, cart):
#         if not self.is_intl:
#             template = 'shipping/usps/request.xml'
#         else:
#             template = 'shipping/usps/request_intl.xml'
#         request = self.render_template(template, cart, contact)
#         self.is_valid = False

#         if settings.LIVE.value:
#             connection = settings.CONNECTION.value
#         else:
#             connection = settings.CONNECTION_TEST.value

#         cache_key_response = "usps-cart-%s-response" % int(cart.id)
#         cache_key_request = "usps-cart-%s-request" % int(cart.id)
#         last_request = cache.get(cache_key_request)

#         tree = cache.get(cache_key_response)

#         if (last_request != request) or tree is None:
#             self.verbose_log("Requesting from USPS [%s]\n%s", cache_key_request, request)
#             cache.set(cache_key_request, request, 60)
#             tree = self._process_request(connection, request)
#             self.verbose_log("Got from USPS [%s]:\n%s", cache_key_response, self.raw)
#             needs_cache = True
#         else:
#             needs_cache = False

#         errors = tree.getiterator('Error')

#         # if USPS returned no error, return the prices
#         if errors == None or len(errors) == 0:
#             # check for domestic results first
#             all_packages = tree.getiterator('RateV3Response')

#             # if there are none, revert to international results
#             if len(all_packages) == 0:
#                 all_packages = tree.getiterator('IntlRateResponse')
#                 for package in all_packages:
#                     for service in package.getiterator('Service'):
#                         #self.verbose_log('%s vs %s' % (service.attrib['ID'], self.service_type_code))
#                         if service.attrib['ID'] == self.service_type_code and \
#                             self.service_type_text.startswith('Int`l: '):
                            
#                             self.charges = service.find('.//Postage').text
#                             self.delivery_days = service.find('.//SvcCommitments').text
#                             #self.verbose_log('%s %s' % (self.charges, self.delivery_days))
#                             self.is_valid = True
#                             self._calculated = True
#                             self.exact_date = True

#                             #if needs_cache:
#                             #    cache.set(cache_key_response, tree, 60)
#             else:
#                 for package in all_packages:
#                     for postage in package.getiterator('Postage'):
#                         if postage.attrib['CLASSID'] == self.service_type_code and \
#                             not self.service_type_text.startswith('Int`l: '):
#                             self.charges = postage.find('.//Rate').text

#                             # Now try to figure out how long it would take for this delivery
#                             if self.api:
#                                 delivery = self.render_template('shipping/usps/delivery.xml', cart, contact)
#                                 del_tree = self._process_request(connection, delivery, self.api)
#                                 parent = '%sResponse' % self.api
#                                 del_iter = del_tree.getiterator(parent)

#                                 if len(del_iter):
#                                     i = del_iter[0]

#                                     # express mail usually has a date commitment
#                                     if self.api == 'ExpressMailCommitment':
#                                         key = './/Date'
#                                         self.exact_date = True
#                                     else:
#                                         key = './/Days'
#                                     if i.find(key) != None:
#                                         self.delivery_days = i.find(key).text

#                             self.is_valid = True
#                             self._calculated = True

#                             #if needs_cache:
#                             #    cache.set(cache_key_response, tree, 60)
#         else:
#             error = errors[0]
#             err_num = error.find('.//Number').text
#             source = error.find('.//Source').text
#             description = error.find('.//Description').text
#             log.info("USPS Error: Code %s: %s" % (err_num, description))





class UPSShipping(object):
    def __init__(self):
        self.raw = None


    def _process_request(self, connection, request):
        """
        Post the data and return the XML response
        """
        log.debug(request)
        conn = urllib2.Request(url=connection, data=request.encode("utf-8"))
        f = urllib2.urlopen(conn)
        all_results = f.read()
        log.debug(all_results)
        self.raw = all_results
        return fromstring(all_results)


    def get_options(self, customer, site, cart):
        site_config = json.loads(site.config_json) if site.config_json else None
        if not site_config: #pragma: no cover
            raise Exception("No site config for UPS Shipping.")
        shipping_config = site_config[0]['shipping']
        campaign = customer.campaign if customer else site.default_campaign
        company = customer.campaign.company if customer else site.company
        xml = util.literal(render('/catalog/shipping.ups_pricing_call.mako',
                                  {'cart' : cart,
                                   'site' : site,
                                   'cust' : customer,
                                   'campaign' : campaign,
                                   'company' : company,
                                   'api_key' : shipping_config['api_key'],
                                   'user_id' : shipping_config['user_id'],
                                   'account' : shipping_config['account'],
                                   'password' : shipping_config['password'],
                                   'container' : shipping_config['container_choices_default'],
                                   'pickup' : shipping_config['pickup_type_choices_default'],
                                   'total_weight' : max(sum([util.nvl(item['product'].weight, 1.0) for item in cart.items]), 1.0)
                                   }))

        tree = self._process_request(shipping_config['ups_url'], xml)
        try:
            status_code = tree.getiterator('ResponseStatusCode')
            status_val = status_code[0].text
        except AttributeError:  #pragma: no cover
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
                    option['orig_charges'] = charges
                    option['charges'] = charges
                    option['delivery_days'] = util.nvl(delivery_days)
                    options.append(option)
        else:  #pragma: no cover
            try:
                errors = tree.find('.//Error')
                log.error("UPS %s Error: Code %s - %s" % (errors[0].text, errors[1].text, errors[2].text))
            except AttributeError:
                log.error("UPS error - cannot parse response:\n %s" % self.raw)

        return cart.filter_shipping_options(options)




