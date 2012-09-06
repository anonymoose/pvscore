#pylint: disable-msg=E1101,R0913
import math
import datetime
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, Date, Float, Text
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel, Session, BaseAnalytic
from app.model.crm.orderitem import OrderItem
from app.model.crm.product import Product, InventoryJournal
from app.model.core.status import Status
import app.lib.util as util
from app.model.crm.journal import Journal
import logging

log = logging.getLogger(__name__)

class CustomerOrder(ORMBase, BaseModel):
    __tablename__ = 'crm_customer_order'
    __pk__ = 'order_id'

    order_id = Column(Integer, primary_key = True)
    customer_id = Column(Integer, ForeignKey('crm_customer.customer_id'))
    campaign_id = Column(Integer, ForeignKey('crm_campaign.campaign_id'))
    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)
    cancel_dt = Column(Date)
    status_id = Column(Integer, ForeignKey('core_status.status_id'))
    user_created = Column(String(50), ForeignKey('core_user.username'))
    note = Column(Text)
    shipping_note = Column(String(50))
    shipping_total = Column(Float)
    handling_note = Column(String(50))
    handling_total = Column(Float)
    external_cart_id = Column(String(100))

    customer = relation('Customer')
    campaign = relation('Campaign')
    creator = relation('Users')
    status = relation('Status', lazy="joined")
    items = relation('OrderItem', lazy="joined", backref=backref('order'), order_by='asc(OrderItem.order_item_id)')
    journal_entries = relation('Journal', lazy="joined", backref=backref('order'), order_by='asc(Journal.journal_id)')

    @staticmethod
    def create_new(cart, customer, site, campaign, user_created, incl_tax=True):
        """ KB: [2010-09-09]: Given a cart full of products, create a new order and return it.
        if a given product is a parent, then create an kid order_item of zero cost and attach it to the parent.
        """
        enterprise_id = site.company.enterprise_id
        cord = CustomerOrder()
        cord.creator = user_created
        cord.customer = customer
        cord.campaign = campaign
        cord.save()
        for cart_item in cart.items:
            prd = Product.load(cart_item['product'].product_id)
            item = OrderItem()
            item.order = cord
            item.product = prd
            item.creator = user_created
            discount = prd.get_discount_price(campaign)
            retail = cart_item['unit_price'] if 'unit_price' in cart_item else prd.get_unit_price(campaign)
            item.quantity = float(cart_item['quantity'])
            item.unit_price = (discount if discount else retail)
            if campaign.tax_rate and incl_tax:
                item.tax = (item.unit_price * item.quantity) * campaign.tax_rate
            item.unit_cost = prd.unit_cost
            item.unit_discount_price = (discount if discount else 0.0)
            item.unit_retail_price = retail

            InventoryJournal.create_new(prd, 'Sale', int(item.quantity), item)
            Status.add(customer, item, Status.find_event(enterprise_id, item, 'CREATED'),
                       'Item added to order %s @ $%s' % (prd.name, util.money(item.unit_price)))
            if prd.can_have_children():
                item.flush() # we need this to get the parent ID.
                children = prd.get_children()
                if children and len(children) > 0:
                    for kid in children:
                        child_item = OrderItem()
                        child_item.order = cord
                        child_item.parent_id = item.order_item_id
                        child_item.product = kid.child
                        child_item.creator = user_created
                        child_item.unit_price = 0.0
                        child_item.unit_discount_price = 0.0
                        child_item.unit_retail_price = 0.0
                        child_item.unit_cost = prd.unit_cost
                        child_item.quantity = kid.child_quantity
                        InventoryJournal.create_new(kid.child, 'Sale', child_item.quantity, child_item)
        Status.add(customer, cord, Status.find_event(enterprise_id, cord, 'CREATED'), 'Order created ')
        cord.save()
        cord.flush()
        return cord


    def augment_order(self, customer, product, campaign, user_created, quantity=0, incl_tax=True):
        enterprise_id = product.company.enterprise_id
        item = OrderItem()
        item.order = self
        item.product = product
        item.creator = user_created
        discount = product.get_discount_price(campaign)
        retail = product.get_price(campaign)
        item.unit_price = (discount if discount else retail)
        if campaign.tax_rate and incl_tax:
            item.tax = (item.unit_price * item.quantity) * campaign.tax_rate
        item.unit_cost = product.unit_cost
        item.unit_discount_price = (discount if discount else 0.0)
        item.unit_retail_price = retail
        item.quantity = quantity
        if quantity > 0:
            InventoryJournal.create_new(product, 'Sale', item.quantity, item)
        item.save()
        if product.can_have_children():
            item.flush() # we need this to get the parent ID.
            children = product.get_children()
            if children and len(children) > 0:
                for kid in children:
                    child_item = OrderItem()
                    child_item.order = self
                    child_item.parent_id = item.order_item_id
                    child_item.product = kid.child
                    child_item.creator = user_created
                    child_item.unit_price = 0.0
                    child_item.unit_discount_price = 0.0
                    child_item.unit_cost = product.unit_cost
                    child_item.quantity = kid.child_quantity
                    InventoryJournal.create_new(kid.child, 'Sale', child_item.quantity, child_item)
        Status.add(customer, self, Status.find_event(enterprise_id, self, 'MODIFIED'), 'Order Modified ')
        self.save()
        self.flush()
        return item


    @staticmethod
    def has_customer_purchased_product(customer, product):
        ret = Session.query("c").from_statement("""select count(0) c from crm_customer_order co, crm_order_item oi
                                                   where co.customer_id = %d
                                                   and co.cancel_dt is null
                                                   and co.order_id = oi.order_id
                                                   and oi.delete_dt is null
                                                   and oi.product_id = %d """ % (customer.customer_id,
                                                                                 product.product_id)).one()
        return ret[0]


    @staticmethod
    def find_by_external_cart_id(external_cart_id):
        return Session.query(CustomerOrder).filter(and_(CustomerOrder.external_cart_id == external_cart_id,
                                                        CustomerOrder.delete_dt == None,
                                                        CustomerOrder.cancel_dt == None)).first()


    @staticmethod
    def find_by_customer(customer, order_id=None, start_dt=None, end_dt=None):
        if order_id:
            return Session.query(CustomerOrder).filter(and_(CustomerOrder.customer==customer,
                                                            CustomerOrder.order_id==order_id)).first()
        else:
            if start_dt and end_dt:
                return Session.query(CustomerOrder).filter(and_(CustomerOrder.customer==customer,
                                                                CustomerOrder.delete_dt==None,
                                                                CustomerOrder.cancel_dt==None,
                                                                CustomerOrder.create_dt >= start_dt,
                                                                CustomerOrder.create_dt >= end_dt))\
                                                               .order_by(CustomerOrder.create_dt.desc()).all()
            else:
                return Session.query(CustomerOrder).filter(and_(CustomerOrder.customer==customer,
                                                                CustomerOrder.delete_dt==None,
                                                                CustomerOrder.cancel_dt==None))\
                                                               .order_by(CustomerOrder.create_dt.desc()).all()


    @property
    def has_subscription(self):
        for oitem in self.active_items:
            if oitem.product.subscription:
                return True
        return False


    @property
    def active_items(self):
        return [oitem for oitem in self.items if oitem.delete_dt is None]


    @property
    def payments_applied(self):
        return len(Journal.filter_payments(self)) > 0


    def apply_discount(self, amount, note=None):
        Journal.create_new(amount, self.customer, self, None, 'Discount', 'Discount', note)
        Status.add(self.customer, self, Status.find_event(self.customer.campaign.company.enterprise_id, self, 'DISCOUNT_APPLIED'),
                   '%s applied: %s' % ('Discount', util.money(amount)))


    @property
    def discounts(self):
        return Journal.filter_discounts(self)


    def total_payments_applied(self):
        return Journal.total_applied(self)


    def total_discounts_applied(self):
        return Journal.total_discounts(self)


    def total_payments_due(self):
        return Journal.total_due(self)


    def total_price(self):
        tot = 0.0
        for oitem in self.active_items:
            tot += (oitem.unit_price * (oitem.quantity if oitem.quantity else 1)) + oitem.tax
        return round(tot + (self.shipping_total if self.shipping_total else 0.0) + (self.handling_total if self.handling_total else 0.0), 2)


    def total_item_price(self):
        tot = 0.0
        for oitem in self.active_items:
            tot += (oitem.unit_price * (oitem.quantity if oitem.quantity else 1))
        return tot


    def total_tax(self):
        tot = 0.0
        for oitem in self.active_items:
            tot += oitem.tax
        return tot


    def total_handling_price(self):
        return (self.handling_total if self.handling_total else 0.0)


    def total_shipping_price(self):
        return (self.shipping_total if self.shipping_total else 0.0)


    def is_customer_deletable(self):
        return True


    def cancel(self, reason, by_customer=False):
        self.cancel_dt = datetime.datetime.date(datetime.datetime.now())
        for oitem in self.active_items:
            prod = oitem.product
            InventoryJournal.create_new(prod, 'Cancelled Order', oitem.quantity, oitem)
            oitem.delete_dt = util.today()
            oitem.save()

        journals = Journal.find_all_by_order(self)
        for j in journals:
            j.delete_dt = util.today()
            j.save()

        msg = 'Order Canceled' if not by_customer else 'Order Cancelled by Customer'
        Status.add(self.customer, self, Status.find_event(self.customer.campaign.company.enterprise_id, self, 'CREATED'), '%s : %s' %(msg, reason))
        self.save()


    @property
    def total(self):
        return self.total_price()


    @property
    def summary(self):
        ret = '<table cellpadding="0" cellspacing="10" border="0"><tr><td><u>Product</u></td><td><u>Quantity</u></td><td><u>Unit Price</u></td><td><u>Item Total</u></td></tr>'
        for i in self.active_items:
            try:
                ret += """<tr>
                            <td nowrap><b>{name}</b></td><td>{quant}</td><td>{price}</td><td align="right">{tot}</td>
                          </tr>
                       """.format(name=i.product.name.encode('ascii', 'ignore'), price=util.money(i.unit_price),
                                  quant=int(i.quantity), tot=util.money(i.total()))
            except Exception as exc:
                log.debug(exc)

        ret += '<tr><td colspan="4"><hr></td></tr>'
        ret += '<tr><td><i>Sub Total</i></td><td colspan="2">&nbsp;</td><td align="right">%s</td></tr>' % util.money(self.total_item_price(), True)
        ret += '<tr><td><i>Shipping/Handling</i></td><td colspan="2">&nbsp;</td><td align="right">%s</td></tr>' % util.money((self.total_shipping_price() + self.total_handling_price()), True)
        ret += '<tr><td><i>Tax</i></td><td colspan="2">&nbsp;</td><td align="right">%s</td></tr>' % util.money(self.total_tax(), True)
        ret += '<tr><td><i>Total Payments</i></td><td colspan="2">&nbsp;</td><td align="right">%s</td></tr>' % util.money(self.total_payments_applied(), True)
        ret += '<tr><td><i>Total Discounts</i></td><td colspan="2">&nbsp;</td><td align="right">%s</td></tr>' % util.money(self.total_discounts_applied(), True)
        ret += '<tr><td><i>Total Due</i></td><td colspan="2">&nbsp;</td><td align="right">%s</td></tr>' % util.money(self.total_payments_due(), True)
        ret += '</table>'
        return ret


    @property
    def payment_history(self):
        try:
            journals = Journal.find_all_by_order(self)
            ret = '<table cellpadding="0" cellspacing="10" border="0"><tr><td><u>Date</u></td><td><u>Method</u></td><td><u>Note</u></td><td><u>Amount</u></td></tr>'
            for j in journals:
                ret += """<tr>
                            <td>{dt}</td><td nowrap>{meth}</td><td>{note}</td><td align="right">{amt}</td>
                          </tr>
                       """.format(dt=util.slash_date(j.create_dt), amt=util.money(j.amount), meth=j.method, note=j.note)
            ret += '<tr><td colspan="4"><hr></td></tr>'
            ret += '<tr><td><i>Total Payments Applied</i></td><td colspan="2">&nbsp;</td><td align="right">%s</td></tr>' % util.money(self.total_payments_applied(), True)
            ret += '</table>'
            return ret
        except Exception as exc:
            log.debug(exc)


class MTDSalesByVendor(BaseAnalytic):
    def __init__(self, request, top=7):
        super(MTDSalesByVendor, self).__init__()
        self.request = request
        self.top = top
        self.run()


    def link(self, height, width, i):
        return "http://{i}.chart.apis.google.com/chart?chxl=0:{google_x_labels}&chxr={google_range}&chxt=y,x&chbh=a,10&chs={height}x{width}&cht=bhs&chco=4D89F9,C6D9FD&chds={google_scale}&chd=t:{google_data}&chma=10,10,10,10&chtt=MTD+Sales+by+Vendor&chts=006699,12.167"\
            .format(google_x_labels=self.google_x_labels,
                    google_range=self.google_range,
                    google_scale=self.google_scale,
                    google_data=self.google_data,
                    height=height,
                    width=width, i=i)

    @property
    def google_range(self):
        max_ = self.col_max('revenue')
        interval = math.floor(max_/10)
        return '0,%s,%s' % (interval, max_+(2*interval))


    @property
    def google_data(self):
        dat1 = ','.join([str(round(util.nvl(res.revenue, 0.0), 2)) for res in self.results])
        dat2 = ','.join([str(round(util.nvl(res.cost, 0.0), 2)) for res in self.results])
        return '%s|%s' % (dat1, dat2)


    @property
    def google_x_labels(self):
        return '|%s' % '|'.join([res.vendor[:10].replace(' ', '+') for res in self.results])


    @property
    def google_scale(self):
        max_ = self.col_max('revenue')
        interval = math.floor(max_/10)
        scale = '%s,%s' % (interval, max_+(2*interval))
        return '%s,%s' % (scale, scale)


    @property
    def columns(self):
        return ("vendor", "cost", "revenue", "profit")


    @property
    def query(self):
        return """select v.name, sum(oi.unit_cost*oi.quantity) as cost,
                           sum(oi.unit_price*oi.quantity) as revenue,
                           sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit
                    from
                    crm_customer_order o, crm_customer cust,
                    crm_order_item oi, crm_campaign cmp,
                    crm_company co, core_status cs, core_status_event cse, crm_product p,
                    crm_vendor v
                    where
                    o.customer_id = cust.customer_id and
                    o.order_id = oi.order_id and
                    o.campaign_id = cmp.campaign_id and
                    oi.product_id = p.product_id and
                    cmp.company_id = co.company_id and
                    co.enterprise_id = {entid} and
                    o.delete_dt is null and
                    oi.delete_dt is null and
                    o.status_id = cs.status_id and
                    cs.event_id = cse.event_id and
                    extract(month from o.create_dt) = extract(month from current_date) and
                    extract(year from o.create_dt) = extract(year from current_date) and
                    p.vendor_id = v.vendor_id
                    group by v.name
                    order by sum(oi.unit_price*oi.quantity) desc""".format(entid=self.request.ctx.enterprise.enterprise_id)




class PeriodOrderSummary(BaseAnalytic):
    """ KB: [2011-11-02]: Google charts report for sales over a period """

    def __init__(self, request, days=7):
        super(PeriodOrderSummary, self).__init__()
        self.request = request
        self.days = days
        self.run()


    def link(self, height, width, i):
        return "http://{i}.chart.apis.google.com/chart?chxl=1:{google_y_labels}&chxr={google_range}&chxt=y,x&chbh=a,10&chs={height}x{width}&cht=bvs&chco=DEE9ED,3D7930&chds={google_scale}&chd=t:{google_data}&chma=10,10,10,10&chtt=Sales+by+Day&chts=006699,12.167"\
            .format(google_y_labels=self.google_y_labels,
                    google_data=self.google_data,
                    google_range=self.google_range,
                    google_scale=self.google_scale,
                    height=height,
                    width=width, i=i)


    @property
    def google_range(self):
        max_ = self.col_max('revenue')
        interval = math.floor(max_/10)
        return '0,%s,%s' % (interval, max_+(2*interval))


    @property
    def google_data(self):
        dat1 = ','.join([str(round(util.nvl(res.revenue, 0.0), 2)) for res in self.results])
        dat2 = ','.join([str(round(util.nvl(res.cost, 0.0), 2)) for res in self.results])
        return '%s|%s' % (dat1, dat2)


    @property
    def google_y_labels(self):
        return '|%s|' % '|'.join([util.format_date(res.create_dt)[5:] for res in self.results])


    @property
    def google_scale(self):
        max_ = self.col_max('revenue')
        interval = math.floor(max_/10)
        scale = '%s,%s' % (interval, max_+(2*interval))
        return '%s,%s' % (scale, scale)


    @property
    def columns(self):
        return ("create_dt", "cost", "revenue", "profit")


    @property
    def query(self):
        return """select o.create_dt, sum(oi.unit_cost*oi.quantity) as cost,
                           sum(oi.unit_price*oi.quantity) as revenue,
                           sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit
                    from
                    crm_customer_order o, crm_customer cust,
                    crm_order_item oi, crm_campaign cmp,
                    crm_company co, core_status cs, core_status_event cse, crm_product p
                    where
                    o.customer_id = cust.customer_id and
                    o.order_id = oi.order_id and
                    o.campaign_id = cmp.campaign_id and
                    oi.product_id = p.product_id and
                    cmp.company_id = co.company_id and
                    co.enterprise_id = {entid} and
                    o.delete_dt is null and
                    oi.delete_dt is null and
                    o.status_id = cs.status_id and
                    cs.event_id = cse.event_id and
                    o.create_dt between current_date - {d} and current_date
                    group by o.create_dt
                    order by o.create_dt asc""".format(d=self.days, entid=self.request.ctx.enterprise.enterprise_id)

