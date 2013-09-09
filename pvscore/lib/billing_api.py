#pylint: disable-msg=W0221,W0613
import urllib
import urllib2
import stripe
import logging
from pyramid.renderers import render
import pvscore.lib.util as util

log = logging.getLogger(__name__)

class BaseBillingApi(object):

    @staticmethod
    def create_api(enterprise):
        """ KB: [2010-10-20]: this is called to get the right api for the application """
        ret = NullBillingApi(enterprise)
        if enterprise is not None:
            if 'Stripe' == enterprise.billing_method:
                ret = StripeBillingApi(enterprise)
            elif 'Authorize.Net' == enterprise.billing_method:
                return AuthorizeNetBillingApi(enterprise)
        return ret


    def purchase(self, order, billing, remote_ip):
        return True


    def get_last_status(self):
        pass


    def set_coupon(self, coupon):
        pass


    def is_declined(self):
        return False


    def create_token(self, enterprise, ccnum, month, year, cvc):  #pylint: disable-msg=R0913
        pass


    def cancel_order(self, order, billing):
        pass


class NullBillingApi(BaseBillingApi):
    def __init__(self, enterprise):
        super(NullBillingApi, self).__init__()
        self.payment_method = 'Credit Card'
        self.coupon = None
        self.enterprise = enterprise


class StripeBillingApi(BaseBillingApi):
    """ KB: [2012-02-10]:
    API for http://stripe.com

    *Recurring Billing*
    To make recurring billing work, ensure you have configured a plan with an ID
    @stripe = product.sku @pvs
    """

    def  __init__(self, enterprise):
        super(StripeBillingApi, self).__init__()
        self.last_status = None
        self.last_note = None
        self.payment_method = 'Credit Card'
        self.coupon = None
        self.enterprise = enterprise


    def create_token(self, ccnum, month, year, cvc):  #pylint: disable-msg=R0913
        stripe.api_key = self.enterprise.get_attr('stripe_private_key')
        token = stripe.Token.create(
            card={
                "number": ccnum,
                "exp_month": month,
                "exp_year": year,
                "cvc": cvc
                },
            )
        return token['id']


    def set_coupon(self, coupon):
        self.coupon = coupon


    def purchase(self, order, billing, cart, remote_ip=None):
        """ KB: [2012-09-10]:
        If it's subscription, then subscribe this customer to the plan.
        Otherwise just hit them up non-recurring.
        """
        if int(order.total_price()) == 0:
            self.payment_method = 'Discount'
            return True   # return that it was successful even though we did nothing.

        if not billing.cc_token:
            raise Exception("No stripe cc_token present")  #pragma: no cover
        campaign = order.campaign
        cust = order.customer
        stripe.api_key = self.enterprise.get_attr('stripe_private_key')

        try:
            # see if this customer exists at stripe.  If not create him.
            stripe_cust = None
            if cust.third_party_id:
                stripe_cust = stripe.Customer.retrieve(cust.third_party_id)
            else:
                stripe_cust = stripe.Customer.create(
                    card=billing.cc_token,
                    description=cust.email
                    )
                cust.third_party_id = stripe_cust.id
                cust.save()

            charge_items_amount = 0.0
            subscription_amount = 0.0
            for oitem in order.active_items:
                if oitem.parent_id is not None:
                    continue
                prod = oitem.product
                if prod.subscription:
                    # if (self.coupon):
                    #     coup = stripe.Coupon.retrieve(self.coupon)
                    #     if coup:
                    #         discount_amount = (float(order.total) * (float(coup.percent_off)/float(100)))
                    #         order.apply_discount(discount_amount, "Discount code = "+self.coupon)
                    #     else:
                    #         self.coupon = None
                    # else:
                    self.coupon = None
                    stripe_cust.update_subscription(plan=prod.sku, coupon=self.coupon)
                    subscription_amount += int(prod.get_price(campaign)*100)
                else:
                    charge_items_amount += int(prod.get_price(campaign)*100)  # must be amount in cents.  whatever.

            if charge_items_amount > 0:
                stripe.Charge.create(
                    customer=stripe_cust.id,
                    amount=int((order.total_price()-subscription_amount)*100),
                    currency="usd",
                    description='%s Purchase' % campaign.company.name)
            return True
        except stripe.CardError as exc:
            self.last_status = exc.code
            self.last_note = exc.message
        except Exception as exc2: #pragma: no cover
            self.last_status = -1
            self.last_note = exc2.message
        return False


    def update_billing(self, cust, bill):
        stripe.api_key = self.enterprise.get_attr('stripe_private_key')
        try:
            if cust.third_party_id:
                stripe_cust = stripe.Customer.retrieve(cust.third_party_id)
                stripe_cust.card = bill.cc_token
                stripe_cust.save()
                return True
        except stripe.CardError as exc:
            self.last_status = exc.code
            self.last_note = exc.message
        except Exception as exc2: #pragma: no cover
            self.last_status = -1
            self.last_note = exc2.message


    def cancel_order(self, order, billing):
        try:
            cust = order.customer
            if not cust.third_party_id:
                return False
            stripe.api_key = self.enterprise.get_attr('stripe_private_key')
            stripe_cust = stripe.Customer.retrieve(cust.third_party_id)
            for oitem in order.active_items:
                prod = oitem.product
                if prod.subscription:
                    stripe_cust.cancel_subscription()
                    return True
        except Exception as exc2: #pragma: no cover
            self.last_note = exc2.message
        return False


    def is_declined(self):
        return (self.last_status is not None or self.last_note is not None)


    def get_last_status(self):
        return (self.last_status, self.last_note)



API_VERSION = '3.1'
DELIM_CHAR = ','
ENCAP_CHAR = '$'
APPROVED, DECLINED, ERROR, FRAUD_REVIEW = 1, 2, 3, 4
RESPONSE_CODE, RESPONSE_REASON_CODE, RESPONSE_REASON_TEXT = 0, 2, 3

#https://github.com/agiliq/merchant/blob/master/docs/gateways/authorize_net.rst
class AuthorizeNetBillingApi(BaseBillingApi):
    test_url = "https://test.authorize.net/gateway/transact.dll"
    live_url = "https://secure.authorize.net/gateway/transact.dll"

    arb_test_url = 'https://apitest.authorize.net/xml/v1/request.api'
    arb_live_url = 'https://api.authorize.net/xml/v1/request.api'

    def  __init__(self, enterprise):
        super(AuthorizeNetBillingApi, self).__init__()
        self.last_status = None
        self.last_note = None
        self.payment_method = 'Credit Card'
        self.coupon = None
        self.enterprise = enterprise
        self.test_mode = ('T' == self.enterprise.get_attr('authnet_test_mode', 'F'))
        self.authnet_login_id = self.enterprise.get_attr('authnet_login_id')
        self.authnet_transaction_key = self.enterprise.get_attr('authnet_transaction_key')


    def set_coupon(self, coupon):
        pass


    def purchase(self, order, billing, cart, remote_ip=None):
        if int(order.total_price()) == 0:
            self.payment_method = 'Discount'
            return True   # return that it was successful even though we did nothing.
        charge_items_amount = 0.0
        subscription_amount = 0.0
        for oitem in order.active_items:
            prod = oitem.product
            if prod.subscription:
                resp = self._create_subscription(prod, oitem, order.customer, billing)
                if not resp:
                    return False
                subscription_amount += int(oitem.total()*100)
            else:
                charge_items_amount += int(oitem.total()*100)  # must be amount in cents.  whatever.

        if charge_items_amount > 0:
            resp = self._charge_card((order.total_price()-subscription_amount), order, order.customer, billing)
            if not resp:
                return False
        return True


    def cancel_order(self, order, billing):
        try:
            cust = order.customer
            for oitem in order.active_items:
                prod = oitem.product
                if prod.subscription:
                    return self._cancel_subscription(cust, order, oitem)
        except Exception as exc2: #pragma: no cover
            self.last_note = exc2.message
        return False  #pragma: no cover


    def update_billing(self, cust, billing):
        try:
            for order in cust.get_active_orders():
                for oitem in order.active_items:
                    prod = oitem.product
                    if prod.subscription:
                        if not self._update_subscription(cust, order, oitem, billing):
                            return False
            return True
        except Exception as exc2: #pragma: no cover
            self.last_note = exc2.message
        return False  #pragma: no cover


    def _update_subscription(self, customer, order, order_item, billing):
        try:
            xml = render('/crm/billing/authnet_arb_update_subscription.xml.mako',
                         {'auth_login' : self.authnet_login_id,
                          'auth_key' : self.authnet_transaction_key,
                          'subscription_id' : order_item.third_party_id,
                          'card_number' : billing.get_cc_num(),
                          'exp_date' : billing.cc_exp
                          })

            headers = {'content-type': 'text/xml'}

            conn = urllib2.Request(url=self._arb_url, data=xml, headers=headers)
            try:
                open_conn = urllib2.urlopen(conn)
                xml_response = open_conn.read()
            except urllib2.URLError: #pragma: no cover
                return (5, '1', 'Could not talk to payment gateway.')

            response = util.xml_str_to_dict(xml_response)['ARBUpdateSubscriptionResponse']
            if response['messages']['resultCode'].lower() != 'ok':
                message = response['messages']['message']
                message = message[0] if type(message) == list else message
                self.last_status = message['code']
                self.last_note = message['text']
                return False
            return True
        except Exception as exc2: #pragma: no cover
            self.last_status = -1
            self.last_note = exc2.message
        return False  #pragma: no cover


    def get_last_status(self):
        return (self.last_status, self.last_note)


    @property
    def _service_url(self):
        return self.test_url if self.test_mode else self.live_url


    @property
    def _arb_url(self):
        return self.arb_test_url if self.test_mode else self.arb_live_url


    def _create_subscription(self, prod, order_item, customer, billing):
        try:
            xml = render('/crm/billing/authnet_arb_create_subscription.xml.mako',
                         {'auth_login' : self.authnet_login_id,
                          'auth_key' : self.authnet_transaction_key,
                          'amount' : order_item.total(),
                          'card_number' : billing.get_cc_num(),
                          'exp_date' : billing.cc_exp,
                          'start_date' : util.format_date(order_item.start_dt) if order_item.start_dt else util.str_today(),
                          'total_occurrences' : 9999,
                          'interval_length' : 1,
                          'interval_unit' : 'months',
                          'sub_name' : '',
                          'first_name' : customer.fname,
                          'last_name' : customer.lname
                          })

            headers = {'content-type': 'text/xml'}

            conn = urllib2.Request(url=self._arb_url, data=xml, headers=headers)
            try:
                open_conn = urllib2.urlopen(conn)
                xml_response = open_conn.read()
            except urllib2.URLError: #pragma: no cover
                return (5, '1', 'Could not talk to payment gateway.')

            response = util.xml_str_to_dict(xml_response)['ARBCreateSubscriptionResponse']
            if response['messages']['resultCode'].lower() != 'ok':
                message = response['messages']['message']
                message = message[0] if type(message) == list else message
                self.last_status = message['code']
                self.last_note = message['text']
                return False
            order_item.third_party_id = response['subscriptionId']
            order_item.save()
            return True
        except Exception as exc2: #pragma: no cover
            self.last_status = -1
            self.last_note = exc2.message
        return False  #pragma: no cover


    def _cancel_subscription(self, customer, order, order_item):
        try:
            xml = render('/crm/billing/authnet_arb_cancel_subscription.xml.mako',
                         {'auth_login' : self.authnet_login_id,
                          'auth_key' : self.authnet_transaction_key,
                          'subscription_id' : order_item.third_party_id
                          })

            headers = {'content-type': 'text/xml'}

            conn = urllib2.Request(url=self._arb_url, data=xml, headers=headers)
            try:
                open_conn = urllib2.urlopen(conn)
                xml_response = open_conn.read()
            except urllib2.URLError: #pragma: no cover
                return (5, '1', 'Could not talk to payment gateway.')

            response = util.xml_str_to_dict(xml_response)['ARBCancelSubscriptionResponse']

            if response['messages']['resultCode'].lower() != 'ok':
                message = response['messages']['message']
                message = message[0] if type(message) == list else message
                self.last_status = message['code']
                self.last_note = message['text']
                return False
            return True
        except Exception as exc2: #pragma: no cover
            self.last_status = -1
            self.last_note = exc2.message
        return False  #pragma: no cover


    def _charge_card(self, amount, order, customer, billing):
        post = {}
        post['invoice_num'] = str(order.order_id)
        post['description'] = "%s Order" % order.campaign.company.name
        post['card_num'] = billing.get_cc_num()
        post['card_code'] = billing.get_cc_cvv()
        post['exp_date'] = billing.cc_exp
        post['first_name'] = customer.fname
        post['last_name'] = customer.lname
        post['address'] = customer.addr1 + ' ' + util.nvl(customer.addr2)
        post['company'] = customer.company_name
        post['phone'] = customer.phone
        post['zip'] = customer.zip
        post['city'] = customer.city
        post['country'] = customer.country
        post['state'] = customer.state
        post['email'] = customer.email
        post['cust_id'] = customer.customer_id
        #post['customer_ip'] = options['ip']
        return self._commit('AUTH_CAPTURE', amount, post)


    def _commit(self, action, money, parameters):
        if not action == 'VOID':
            parameters['amount'] = money
        parameters['test_request'] = self.test_mode
        url = self._service_url
        data = self._post_data(action, parameters)
        response = self._request(url, data)
        if response['response_code'] != 1:
            self.last_status = response['response_code']
            self.last_note = response['response_reason_text']
            return False
        return True


    def _post_data(self, action, parameters=None):
        """add API details, gateway response formating options
        to the request parameters"""
        if not parameters:
            parameters = {}   #pragma: no cover
        post = {}
        post['version'] = API_VERSION
        post['login'] = self.authnet_login_id
        post['tran_key'] = self.authnet_transaction_key
        post['relay_response'] = "FALSE"
        post['type'] = action
        post['delim_data'] = "TRUE"
        post['delim_char'] = DELIM_CHAR
        post['encap_char'] = ENCAP_CHAR
        post.update(parameters)
        return urllib.urlencode(dict(('x_%s' % (k), v) for k, v in post.iteritems()))


    def _request(self, url, data, headers=None):
        """Make POST request to the payment gateway with the data and return
        gateway RESPONSE_CODE, RESPONSE_REASON_CODE, RESPONSE_REASON_TEXT"""
        if not headers:
            headers = {}
        conn = urllib2.Request(url=url, data=data, headers=headers)
        try:
            open_conn = urllib2.urlopen(conn)
            response = open_conn.read()
        except urllib2.URLError: #pragma: no cover
            return (5, '1', 'Could not talk to payment gateway.')
        fields = response[1:-1].split('%s%s%s' % (ENCAP_CHAR, DELIM_CHAR, ENCAP_CHAR))
        return self._save_authorize_response(fields)


    def _save_authorize_response(self, response):
        data = {}
        data['response_code'] = int(response[0])
        data['response_reason_code'] = response[2]
        data['response_reason_text'] = response[3]
        data['authorization_code'] = response[4]
        data['address_verification_response'] = response[5]
        data['transaction_id'] = response[6]
        data['invoice_number'] = response[7]
        data['description'] = response[8]
        data['amount'] = response[9]
        data['method'] = response[10]
        data['transaction_type'] = response[11]
        data['customer_id'] = response[12]

        data['first_name'] = response[13]
        data['last_name'] = response[14]
        data['company'] = response[15]
        data['address'] = response[16]
        data['city'] = response[17]
        data['state'] = response[18]
        data['zip_code'] = response[19]
        data['country'] = response[20]
        data['phone'] = response[21]
        data['fax'] = response[22]
        data['email'] = response[23]

        data['shipping_first_name'] = response[24]
        data['shipping_last_name'] = response[25]
        data['shipping_company'] = response[26]
        data['shipping_address'] = response[27]
        data['shipping_city'] = response[28]
        data['shipping_state'] = response[29]
        data['shipping_zip_code'] = response[30]
        data['shipping_country'] = response[31]
        data['card_code_response'] = response[38]
        return data
# """
# Gateway run by Matt Piruvil (mpirvul@eaccounts.net)
# API documentation : https://admin.eaccounts.net/apiconf.php
# API details: https://admin.eaccounts.net/api.php
# Response Codes: https://admin.eaccounts.net/info.php
# $arrTransaction = array(
#     'name' => 'WealthMakers.com',
#     'address' => '2213 Via Blanca',
#     'city' => 'Oceanside',
#     'state' => 'CA',
#     'zip' => '92054',
#     'amount' => '1.01',
#     'account' => '4812099850079113',
#     'month' => 11,
#     'year' => 06,
#     'code' => '252',
#     'phone' => '760-429-4660',
#     'ip' => '69.180.76.55',
#     'email' => 'billing@wealthmakers.com',
#     'reference' => 'transaction id' # should be your unique id for the transaction
# );

# """
# class EAccountsBillingApi(BaseBillingApi):
#     def __init__(self):
#         self.payment_method = 'Credit Card'

#     def cancel_order(self, order, billing):
#         return False

#     def set_coupon(self, coupon):
#         self.coupon = coupon

#     """
#     def create_account(self, cust, billing, handler, remote_ip=None):
#         cc_exp = billing.cc_exp.split('/')
#         vars = {'v': 2,
#                 'key': config['app_conf']['pvs.billing.eaccounts.key1'],
#                 'pass': config['app_conf']['pvs.billing.eaccounts.key2'],
#                 #'reference': '%d' % order.order_id,
#                 #'authorized': 'true',
#                 'name': billing.account_holder,
#                 'address': billing.account_addr,
#                 'city': billing.account_city,
#                 'state': billing.account_state,
#                 'zip': billing.account_zip,
#                 #'amount': order.total_price(),
#                 'account': billing.get_credit_card_number(),
#                 'month': cc_exp[0],
#                 'year': cc_exp[1],
#                 'code': billing.get_credit_card_cvv(),
#                 'phone': cust.phone,
#                 'ip': remote_ip,
#                 'email': cust.email}

#         # new api for recurring billing.
#         #http://realtime.eaccounts.net/administration.php?key=5E7B461B-BC66-4161-8C0F-59C6CB38BBB3&pass=F9E1FA49-6C2F-4B03-95E1-890253AA2601&object=recurring&action=update&recurring=612683&comments=Test+comment+ammendment&tracking=1Z5349857384752435&reference=FDS VDSF
#         # size     = 0  run it every month
#         # date     = the start date.    leave it blank for "start now"
#         # interval =  see text box values
#         # active   = is recurring billing on or not '1'
#         # object   = (transaction, recurring)  [transaction not ready yet.]
#         # action   = (update, search, create)

#         url = config['app_conf']['pvs.billing.eaccounts.url']
#         qstr = '?'
#         for k in vars.keys():
#             qstr = '{qstr}{k}={v}&'.format(qstr=qstr, k=k, v=urllib.quote_plus(str(vars[k])))
#         url = '{url}{qstr}'.format(url=url, qstr=qstr)
#         r = urllib.urlopen(url)
#         resp = self._parse_response(r.readlines())
#         hist = self._create_history(resp, None, billing, cust)
#         return handler(self, resp, hist, None, billing)
#     """

#     """ KB: [2010-10-20]: Keys are kept in the ini file """
#     def purchase(self, order, billing, handler, remote_ip=None):
#         cust = order.customer
#         cc_exp = billing.cc_exp.split('/')

#         url = "https://realtime.eaccounts.net/"
#         v = {'v': 2,
#              'key': config['app_conf']['pvs.billing.eaccounts.key1'],
#              'pass': config['app_conf']['pvs.billing.eaccounts.key2'],
#              'reference': '%d' % order.order_id,
#              #'authorized': 'true',
#              'name': billing.account_holder,
#              'address': billing.account_addr,
#              'city': billing.account_city,
#              'state': billing.account_state,
#              'zip': billing.account_zip,
#              'amount': order.total_price(),
#              'account': billing.get_credit_card_number(),
#              'month': cc_exp[0],
#              'year': cc_exp[1],
#              'code': billing.get_credit_card_cvv(),
#              'phone': cust.phone,
#              'ip': remote_ip,
#              'email': cust.email}

#         resp = self._request(url, v)
#         resp = self._parse_non_recurring_response(resp)
#         hist = self._create_history(resp, order, billing, cust)
#         non_recurring_result = handler(self, resp, hist, order, billing)

#         non_recurring_result = True
#         if non_recurring_result and order.has_subscription and order.active_items[0].product.subscription == True:
#             # we only support one recurring item per order.
#             url = 'https://api.eaccounts.net'
#             v = {'business': config['app_conf']['pvs.billing.eaccounts.subscription.business'],
#                  'user': config['app_conf']['pvs.billing.eaccounts.subscription.user'],
#                  'object': 'recurring',
#                  'action': 'create',
#                  'comments': '%d' % order.order_id,
#                  'descriptor': order.active_items[0].product.name,
#                  'reference': '%d' % order.order_id,
#                  'active': '1',
#                  'size': '0',
#                  'begin': str(util.today_date() + datetime.timedelta(days=28)), #add 28 days to today for our first recurring record.
#                  'interval': '1m',
#                  'name': billing.account_holder,
#                  'address': billing.account_addr,
#                  'city': billing.account_city,
#                  'state': billing.account_state,
#                  'zip': billing.account_zip,
#                  'send': '1',
#                  'amount': order.total_price(),
#                  'account': billing.get_credit_card_number(),
#                  'month': cc_exp[0],
#                  'year': cc_exp[1],
#                  'code': billing.get_credit_card_cvv(),
#                  'phone': cust.phone,
#                  'ip': remote_ip,
#                  'email': cust.email}
#             resp = self._request(url, v)
#             resp = self._parse_recurring_response(resp)
#             billing.cc_token = resp['recurring']
#             Status.add(cust, order, Status.find_event(cust, 'NOTE'),
#                        'Recurring Billing Configured.  EAccounts Reference = %s' % billing.cc_token)
#             billing.save()
#             billing.commit()

#         return non_recurring_result

#     def _request(self, url, v):
#         qstr = '?'
#         for k in v.keys():
#             qstr = '{qstr}{k}={v}&'.format(qstr=qstr, k=k, v=urllib.quote_plus(str(v[k])))
#         url = '{url}{qstr}'.format(url=url, qstr=qstr)
#         r = urllib.urlopen(url)
#         return r.readlines()

#     def cancel_order(self, order, billing):
#         try:
#             cust = order.customer
#             if not billing or not billing.cc_token: return False
#             url = 'https://api.eaccounts.net'
#             v = {'business': config['app_conf']['pvs.billing.eaccounts.subscription.business'],
#                  'user': config['app_conf']['pvs.billing.eaccounts.subscription.user'],
#                  'object': 'recurring',
#                  'action': 'update',
#                  'recurring': billing.cc_token,
#                  'active': '0'}

#             resp = self._request(url, v)
#             #billing.cc_token = resp.recurring
#             return True
#         except Exception as e2:
#             raise
#         return False

#     def update_billing(self,cust, bill):
#         return True

#     def _create_history(self, resp, order, billing, customer):
#         from pvscore.model.crm.billing import BillingHistory
#         self.last_status = urllib.unquote_plus(resp['status'])
#         self.last_note = urllib.unquote_plus(resp['notes'])
#         h = BillingHistory()
#         h.order = order
#         h.billing = billing
#         h.customer = customer
#         h.status_msg = self.last_status
#         h.parent = resp['parent']
#         h.reference = resp['reference']
#         h.notes = self.last_note
#         h.amount = resp['amount']
#         h.authorized = resp['authorized']
#         h.date = urllib.unquote_plus(resp['date'])
#         h.transaction = resp['transaction']
#         h.uid = resp['uid']
#         h.save()
#         h.commit()
#         return h

#     """ KB: [2010-10-20]:
#     {
#      'status': '04%2FDeclined'
#      'account': '411111..1111'
#      'transaction': '707989'
#      'parent': ''
#      'reference': 'ORD-35'
#      'notes': '011%2FOver+Daily+%7C+Activity+Limit%2F65%2F++++DECLINE+++++'
#      'tax': '0'
#      'shipping': '0'
#      'avs': '0'
#      'amount': '30.000'
#      'authorized': '0'
#      'date': '2010-10-20+12%3A32%3A52'
#      'id': '707989'
#      'uid': '7CE482FE-BF05-458A-8455-FBBB3B905649'
#      }
#     """
#     def _parse_non_recurring_response(self, response_lines):
#         if len(response_lines) == 1:
#             kv_pre = response_lines[0].split('&')
#             response = {}
#             for kv in kv_pre:
#                 kv = kv.split('=')
#                 response[kv[0]] = urllib.unquote_plus(str(kv[1]))
#         return response

#     """ KB: [2012-07-06]:
#     ['recurring=1250&descriptor=Power+Trader+2&name=Ken+Bedwell&address=123+Elm&city=Ponte+Vedra+Beach&state=FL&zip=32081&phone=9047167487&email=k1%40test.com&send=1&ip=127.0.0.1&type=1&account=4101111111111111&month=02&year=2013&date=2012-08-03&amount=99.0&comments=265255&active=1&interval=1m&begin=2012-08-03&code=123&business=5D9C6121-F453-4BDD-BE2F-82C94ED5B30E&user=135080C5-869F-4F43-B683-D1446C5769B4&request=730&records=1']
#     """
#     def _parse_recurring_response(self, response_lines):
#         if len(response_lines) == 1:
#             kv_pre = response_lines[0].split('&')
#             response = {}
#             for kv in kv_pre:
#                 kv = kv.split('=')
#                 response[kv[0]] = urllib.unquote_plus(str(kv[1]))
#         return response

#     def is_declined(self, response_dict):
#         if 'status' in response_dict:
#             r = response_dict['status']
#             return r != '01/Authorized'

#     def get_last_status(self):
#         return (self.last_status, self.last_note)
