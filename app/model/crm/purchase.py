#pylint: disable-msg=E1101,R0913
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, Date, Text, Float, Boolean
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel, Session
from app.model.crm.company import Company
from app.lib.dbcache import FromCache, invalidate
import logging

log = logging.getLogger(__name__)


class PurchaseOrder(ORMBase, BaseModel):
    __tablename__ = 'crm_purchase_order'
    __pk__ = 'purchase_order_id'

    purchase_order_id = Column(Integer, primary_key = True)
    note = Column(String(2000))
    company_id = Column(Integer, ForeignKey('crm_company.company_id'))
    create_dt = Column(Date, server_default=text('now()'))
    delete_dt = Column(Date)
    vendor_id = Column(Integer, ForeignKey('crm_vendor.vendor_id'))
    status_id = Column(Integer, ForeignKey('core_status.status_id'))
    shipping_cost = Column(Float)
    tax_cost = Column(Float)
    complete_dt = Column(Date)
    cancel_dt = Column(Date)

    company = relation('Company', lazy='joined')
    status = relation('Status')
    vendor = relation('Vendor')


    @staticmethod
    def search(enterprise_id, vendor_id, from_dt, to_dt):
        v_clause = f_clause = t_clause = ''
        if vendor_id:
            v_clause = "and po.vendor_id = %s" % vendor_id
        if from_dt:
            f_clause = "and po.create_dt >= '%s'" % from_dt
        if to_dt:
            t_clause = "and po.create_dt <= '%s'" % to_dt

        sql = """SELECT po.* FROM crm_purchase_order po, crm_company com
                 where  po.company_id = com.company_id
                 and com.enterprise_id = {ent_id}
                 {v} {f} {t} order by po.purchase_order_id""".format(v=v_clause, f=f_clause, 
                                                                     t=t_clause, ent_id=enterprise_id)
        return Session.query(PurchaseOrder).from_statement(sql).all()


    def total(self):
        tot = 0
        for poi in self.order_items:
            tot += poi.total()
        return tot


    @staticmethod
    def find_all_open(enterprise_id):
        return Session.query(PurchaseOrder)\
            .options(FromCache('PurchaseOrder.find_all_open', enterprise_id)) \
            .join((Company, PurchaseOrder.company_id == Company.company_id)) \
            .filter(and_(PurchaseOrder.delete_dt == None, 
                         Company.enterprise_id == enterprise_id
                         )) \
                         .order_by(PurchaseOrder.purchase_order_id.desc()) \
                         .all()

                         
    @staticmethod
    def full_delete(purchase_order_id):
        Session.execute('delete from crm_purchase_order_item where purchase_order_id = %s' % purchase_order_id)
        Session.execute('delete from crm_purchase_order where purchase_order_id = %s' % purchase_order_id)


    def invalidate_caches(self, **kwargs):
        invalidate(self, 'PurchaseOrder.find_all_open', self.company.enterprise_id)


class PurchaseOrderItem(ORMBase, BaseModel):
    __tablename__ = 'crm_purchase_order_item'
    __pk__ = 'order_item_id'

    order_item_id = Column(Integer, primary_key=True)
    purchase_order_id = Column(Integer, ForeignKey('crm_purchase_order.purchase_order_id'))
    product_id = Column(Integer, ForeignKey('crm_product.product_id'))
    quantity = Column(Float, default=1.0)
    unit_cost = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    status_id = Column(Integer, ForeignKey('core_status.status_id'))
    note = Column(String(100))
    create_dt = Column(Date, server_default=text('now()'))
    delete_dt = Column(Date)
    complete_dt = Column(Date)
    cancel_dt = Column(Date)

    product = relation('Product')
    purchase_order = relation('PurchaseOrder', lazy='joined', backref=backref('order_items', order_by='PurchaseOrderItem.order_item_id'))


    def total(self):
        try:
            return self.unit_cost * self.quantity
        except Exception as exc:
            log.debug(exc)
            return 0.0

    @staticmethod
    def find_by_product(product):
        return Session.query(PurchaseOrderItem)\
            .join((PurchaseOrder, PurchaseOrder.purchase_order_id == PurchaseOrderItem.purchase_order_id)) \
            .filter(and_(PurchaseOrder.delete_dt == None, 
                         PurchaseOrderItem.delete_dt == None,
                         PurchaseOrderItem.product == product
                         )) \
                         .order_by(PurchaseOrder.create_dt.desc()) \
                         .all()


    @staticmethod
    def create_new(purchase_order, product, quantity, unit_cost, discount=0.0, note=None):
        poi = PurchaseOrderItem()
        poi.purchase_order = purchase_order
        poi.product = product
        poi.quantity = quantity
        poi.unit_cost = unit_cost
        poi.discount = discount
        poi.note = note
        poi.save()
        return poi

class Vendor(ORMBase, BaseModel):
    __tablename__ = 'crm_vendor'
    __pk__ = 'vendor_id'

    vendor_id = Column(Integer, primary_key=True)
    enterprise_id = Column(Integer, ForeignKey('crm_enterprise.enterprise_id'))
    name = Column(String(100))
    addr1 = Column(String(50))
    addr2 = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(50))
    country = Column(String(50))
    phone = Column(String(20))
    alt_phone = Column(String(20))
    fax = Column(String(20))
    email = Column(String(50))
    url = Column(String(100))
    note = Column(Text)
    revshare = Column(Float)
    create_dt = Column(Date, server_default=text('now()'))
    delete_dt = Column(Date)
    send_month_end_report = Column(Boolean, default=False)
    
    enterprise = relation('Enterprise')


    @staticmethod
    def find_all(enterprise_id):
        return Session.query(Vendor).options(FromCache('Vendor.find_all', enterprise_id)) \
            .filter(and_(Vendor.delete_dt == None, 
                         Vendor.enterprise_id == enterprise_id
                         )) \
                         .order_by(Vendor.name) \
                         .all()


    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Vendor.find_all', self.enterprise_id)

