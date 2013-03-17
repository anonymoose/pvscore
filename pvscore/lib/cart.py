import datetime, operator
import pvscore.lib.util as util
from pvscore.model.crm.discount import Discount


class Cart(object):

    def __init__(self, site=None):
        self.items = []
        self.site_id = site.site_id if site else None
        self.discount = None
        self.discount_id = None
        self.is_user_discount = False
        self.shipping_options = None
        self.shipping_selection = None
        self.shipping_addr1 = None
        self.shipping_addr2 = None
        self.shipping_city = None
        self.shipping_state = None
        self.shipping_zip = None
        self.shipping_country = None
        self.shipping_phone = None


    @property
    def item_count(self):
        return len(self.items)


    def add_item(self, product, campaign, quantity=1, base_price=None, start_dt=None, attributes={}, note=None): #pylint: disable-msg=R0913,W0102
        """ KB: [2013-02-24]: attribute_ids == {'123abc...' : 3, ...}  where 3 is the quantity """
        if not base_price:
            base_price = product.get_price(campaign)
        base_price = float(base_price)
        unit_price = base_price
        quantity = float(quantity)
        discount_price = product.get_discount_price(campaign)
        if discount_price is not None and round(discount_price, 2) < round(unit_price, 2):
            unit_price = discount_price

        self.items.append({'product': product,
                           'quantity': quantity,
                           'campaign_id': campaign.campaign_id,
                           'attributes': attributes, 
                           'dt': datetime.datetime.date(datetime.datetime.now()),
                           'base_price':base_price,
                           'unit_price':unit_price,
                           'note' : note,
                           'discount_amount':(base_price-unit_price)*quantity,
                           'regular_price':round(base_price*quantity, 2),
                           'price': round(unit_price*quantity, 2),
                           'start_dt':util.parse_date_as_date(util.nvl(str(start_dt), util.str_today())),
                           'handling':(product.handling_price if product.handling_price else 0)*quantity,
                           'weight':(product.weight if product.weight else 0) * quantity})
        self.shipping_options = None
        self.shipping_selection = None


    def set_user_discount(self, discount):
        self.discount = discount
        if discount:
            self.is_user_discount = True


    def inspect_cart_discounts(self, enterprise_id):
        """ KB: [2013-03-11]: Look for cart discounts.
        Call this before rendering shipping and the final totals so you can see if there are any shipping discounts
        """
        if self.is_user_discount:
            return
        applicable_total = self.product_total + self.handling_total
        cart_discounts = sorted([disc for disc in Discount.find_all_automatic_cart_discounts(enterprise_id) if applicable_total > disc.cart_minimum],
                                key=operator.attrgetter('percent_off'), reverse=True)
        if len(cart_discounts) > 0:
            self.discount = cart_discounts[0]


    def calculate_cart_discount_shipping_price(self, shipping_charge): #pylint: disable-msg=C0103
        """ KB: [2013-03-12]: If there is a discount on shipping then use it.  Otherwise pass through. """
        if self.discount and self.discount.shipping_percent_off:
            return float(shipping_charge) - (float(shipping_charge) * (self.discount.shipping_percent_off/100.0))
        return float(shipping_charge)


    def filter_shipping_options(self, options):
        """ KB: [2013-03-12]: Return appropriate options. If it's 100% off shipping, then return only the cheapest option."""
        cheapest_option = None
        cheapest_option_charge = None
        for option in options:
            option['charges'] = self.calculate_cart_discount_shipping_price(option['charges'])
            if not cheapest_option or float(option['orig_charges']) < cheapest_option_charge:
                cheapest_option = option
                cheapest_option_charge = float(option['charges'])
        if self.discount and self.discount.shipping_percent_off and int(self.discount.shipping_percent_off) == 100:
            return [cheapest_option]
        return options
    

    def calculate_cart_discount_for_order(self, order): #pylint: disable-msg=C0103
        if self.discount and self.discount.cart_discount:
            order.discount_id = self.discount.discount_id
            order.discount_percent_off = self.discount.percent_off
            order.discount_shipping_percent_off = self.discount.shipping_percent_off


    def remove_all(self):
        del self.items
        self.items = []
        self.shipping_options = None
        self.shipping_selection = None


    @property
    def shipping_selection_name(self):
        if self.shipping_options and self.shipping_selection:
            for opt in self.shipping_options:
                if opt['code'] == self.shipping_selection:
                    return opt['name']


    @property
    def shipping_total(self):
        if self.shipping_options and self.shipping_selection:
            for opt in self.shipping_options:
                if opt['code'] == self.shipping_selection:
                    return float(opt['charges'])
        return 0.0


    @property
    def shipping_discount_total(self):
        if self.shipping_options and self.shipping_selection:
            for opt in self.shipping_options:
                if opt['code'] == self.shipping_selection:
                    return float(opt['orig_charges']) - float(opt['charges'])
        return 0.0


    @property
    def total(self):
        return self.product_total + self.handling_total + self.shipping_total


    @property
    def product_base_total(self):
        return util.nvl(reduce(lambda x, y: x + y['regular_price'], self.items, 0.0), 0.0)


    @property
    def product_total(self):
        return util.nvl(reduce(lambda x, y: x + y['price'], self.items, 0.0), 0.0)


    @property
    def handling_total(self):
        return util.nvl(reduce(lambda x, y: x + y['handling'], self.items, 0.0), 0.0)


    @property
    def product_discount_total(self):
        return util.nvl(reduce(lambda x, y: x + y['discount_amount'], self.items, 0.0), 0.0)


    def has_product_id(self, product_id):
        return len([item for item in self.items if item['product'].product_id == product_id]) > 0


    def remove_item(self, product):
        found = False
        for i in range(len(self.items)-1, -1, -1):
            if str(self.items[i]['product'].product_id) == str(product.product_id):
                del(self.items[i])
                self.shipping_options = None
                self.shipping_selection = None
                found = True
        return found

