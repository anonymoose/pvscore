#pylint: disable-msg=W0221,W0613
import stripe
import logging

log = logging.getLogger(__name__)

class BaseBillingApi(object):

    @staticmethod
    def create_api(enterprise):
        """ KB: [2010-10-20]: this is called to get the right api for the application """
        ret = NullBillingApi()
        if (enterprise is not None and 'Stripe' == enterprise.billing_method):
            ret = StripeBillingApi()
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
    def __init__(self):
        super(NullBillingApi, self).__init__()
        self.payment_method = 'Credit Card'
        self.coupon = None


class StripeBillingApi(BaseBillingApi):
    """ KB: [2012-02-10]:
    API for http://stripe.com
    
    *Recurring Billing*
    To make recurring billing work, ensure you have configured a plan with an ID
    @stripe = product.sku @pvs
    """

    def  __init__(self):
        super(StripeBillingApi, self).__init__()
        self.last_status = None
        self.last_note = None
        self.payment_method = 'Credit Card'
        self.coupon = None


    def create_token(self, enterprise, ccnum, month, year, cvc):  #pylint: disable-msg=R0913
        stripe.api_key = enterprise.get_attr('stripe_private_key')
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
        if not billing.cc_token:
            raise Exception("No stripe cc_token present")  #pragma: no cover
        campaign = order.campaign
        cust = order.customer
        stripe.api_key = cust.campaign.company.enterprise.get_attr('stripe_private_key')

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
        stripe.api_key = cust.campaign.company.enterprise.get_attr('stripe_private_key')
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
            stripe.api_key = cust.campaign.company.enterprise.get_attr('stripe_private_key')
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
