#pylint: disable-msg=E1101,C0103
import logging
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, DateTime, Text, Boolean, DateTime, Float
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.model.core.asset import Asset
#from pvscore.lib.sphinx.sphinxapi import *
import pvscore.lib.db as db
#from pvscore.model.core.attribute import AttributeValue
import uuid
from md5 import md5
from pvscore.lib.sqla import GUID

log = logging.getLogger(__name__)

class Listing(ORMBase, BaseModel):
    __tablename__ = 'pvs_listing'
    __pk__ = 'listing_id'

    listing_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    customer_id = Column(GUID, ForeignKey('crm_customer.customer_id'))
    company_id = Column(GUID, ForeignKey('crm_company.company_id'))
    site_id = Column(GUID, ForeignKey('cms_site.site_id'))
    status_id = Column(GUID, ForeignKey('core_status.status_id'))
    title = Column(String(255))
    description = Column(Text)
    category = Column(String(50))
    keywords = Column(String(250))
    location = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    show_location = Column(Boolean)
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(50))
    country = Column(String(50))
    ip = Column(String(15))
    dma = Column(Integer)
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)

    customer = relation('Customer')
    company = relation('Company')
    status = relation('Status')
    site = relation("Site")


    @property
    def hash(self):
        salt = 'derf'
        return md5('%s%s%s%s' % (self.company_id, self.customer_id, self.listing_id, salt)).hexdigest()


    @staticmethod
    def find_by_customer(customer):
        return Session.query(Listing).filter(and_(Listing.customer == customer,
                                                  Listing.delete_dt == None))\
                                                  .order_by(Listing.create_dt.desc()).all()


    @property
    def assets(self):
        return Asset.find_for_object(self)


    @staticmethod
    def find_last_n_assets(last_n):
        return db.get_list("""select a.id from core_asset a
                              where a.fk_type = 'Listing'
                              and a.fk_id is not null
                              and create_dt > (current_date - %s)
                              order by create_dt desc """ % last_n)


    @staticmethod
    def find_all_pending_approval(enterprise_id):
        return db.get_object_list(Listing,
                                  """select l.*
                                    from pvs_listing l, core_status s, core_status_event e, crm_company c, crm_enterprise ent, core_asset a
                                    where l.status_id = s.status_id
                                    and a.fk_type = 'Listing'
                                    and a.fk_id = l.listing_id
                                    and s.event_id = e.event_id
                                    and l.company_id = c.company_id
                                    and c.enterprise_id = ent.enterprise_id
                                    and l.delete_dt is null
                                    and e.short_name not in ('CLOSED', 'OPEN', 'APPROVED', 'DECLINED')
                                    and ent.enterprise_id = '%s' order by l.create_dt""" % enterprise_id)


    @staticmethod
    def full_delete(listing_id):
        Session.execute("delete from pvs_listing where listing_id = '%s'" % listing_id)



    # @staticmethod
    # def find_by_title_and_description_and_keywords(title, description, keywords, company):
    #     """ KB: [2012-07-20]: This sucks completely. """
    #     olist = db.get_object_list(Listing, """
    #                 select * from pvs_listing where
    #                  trim(both from title) = trim(both from '{title}')
    #                 and company_id = {company_id} and delete_dt is null
    #                 """.format(title=db.clean(title),
    #                            description=db.clean(description),
    #                            keywords=db.clean(keywords),
    #                            company_id=company.company_id))
    #     if olist:
    #         return olist[0]

    # def is_favorite(self, customer):
    #     return ListingFavorite.is_favorite(customer, self)

    # @staticmethod
    # def find_by_attr(attr_name, attr_value):
    #     listing_id = AttributeValue.find_fk_id_by_value('Listing', attr_name, attr_value)
    #     if listing_id:
    #         return Listing.load(listing_id)


    # """ KB: [2011-07-13]: For now, just stuff it in Redis. """
    # def record_hit(self, ip, geo_ip, is_mobile):
    #     now = util.now()
    #     Redis.hincrby('LISTING:cmp|%s:c|%s:l|%s:y|%s:m|%s:d|%s'\
    #                       % (self.company_id, self.customer_id, self.listing_id, now.year, now.month, now.day), '.', 1)
    #     Redis.hincrby('LISTING:cmp|%s:c|%s:l|%s'\
    #                       % (self.company_id, self.customer_id, self.listing_id), '.', 1)

    # @property
    # def hit_count(self):
    #     val = Redis.hget('LISTING:cmp|%s:c|%s:l|%s'\
    #                           % (self.company_id, self.customer_id, self.listing_id), '.')
    #     return val if val else 0

    # @property
    # def hit_count_today(self):
    #     now = util.now()
    #     val = Redis.hget('LISTING:cmp|%s:c|%s:l|%s:y|%s:m|%s:d|%s'\
    #                           % (self.company_id, self.customer_id, self.listing_id, now.year, now.month, now.day), '.')
    #     return val if val else 0

    # @staticmethod
    # def _search_impl(kw, category, lat, lng, limit, radius_mi):
    #     cl = SphinxClient()
    #     cl.SetServer('localhost', 9312)
    #     #cl.SetMatchMode(SPH_MATCH_ALL)
    #     cl.SetMatchMode(SPH_MATCH_EXTENDED2)
    #     cl.SetLimits(0, limit, 100)
    #     cl.SetGeoAnchor('latitude', 'longitude', math.radians(lat), math.radians(lng))
    #     circle = radius_mi * 1609.344
    #     cl.SetFilterFloatRange('@geodist', 0.0, circle)
    #     if category:
    #         if kw:
    #             q = '@category {cat} @(title,description) {kw}'.format(cat=category, kw=kw)
    #         else:
    #             q = '@category {cat}'.format(cat=category, kw=kw)
    #     else:
    #         q = '@(title,description) {kw}'.format(kw=kw)

    #     res = cl.Query(q, '*')
    #     if res and 'matches' in res and len(res['matches']) > 0:
    #         return [str(m['id']) for m in res['matches']]

    # @staticmethod
    # def search(kw, category, lat, lng, radius_mi=10.0):  #radius in miles
    #     # change this limit to something user configurable.
    #     listing_ids = Listing._search_impl(kw, category, lat, lng, 20, radius_mi)
    #     if listing_ids and len(listing_ids) > 0:
    #         return Session.query(Listing)\
    #             .filter(Listing.listing_id.in_(listing_ids)).all()

    # @staticmethod
    # def search_related(primary_search_results, kw, category, lat, lng, limit, radius_mi=100.0):
    #     listing_ids = Listing._search_impl(kw, category, lat, lng, limit, radius_mi)
    #     if listing_ids and len(listing_ids) > 0:
    #         other_clause = ''
    #         if primary_search_results and len(primary_search_results) > 0:
    #             other_ids = [str(lst.listing_id) for lst in primary_search_results]
    #             return Session.query(Listing)\
    #                 .filter(and_(Listing.listing_id.in_(listing_ids),
    #                              not_(Listing.listing_id.in_(other_ids)))).all()
    #         else:
    #             return Session.query(Listing)\
    #                 .filter(Listing.listing_id.in_(listing_ids)).all()



#class ListingFavorite(ORMBase, BaseModel):
#    __tablename__ = 'pvs_listing_favorite'
#    __pk__ = 'favorite_id'
#
#    favorite_id = Column(Integer, primary_key = True)
#    listing_id = Column(Integer, ForeignKey('pvs_listing.listing_id'))
#    customer_id = Column(Integer, ForeignKey('crm_customer.customer_id'))
#    create_dt = Column(DateTime, server_default = text('now()'))
#    delete_dt = Column(DateTime)
#
#
#    @staticmethod
#    def create_new(customer, listing):
#        lf = ListingFavorite()
#        lf.customer_id = customer.customer_id
#        lf.listing_id = listing.listing_id
#        lf.save()
#        return lf
#
#
#    @staticmethod
#    def find_favorite(customer, listing):
#        return Session.query(ListingFavorite).filter(and_(ListingFavorite.customer_id == customer.customer_id,
#                                                          ListingFavorite.listing_id == listing.listing_id)).first()
#
#
#    @staticmethod
#    def is_favorite(customer, listing):
#        return (0 < ListingFavorite.count('where customer_id = %d and listing_id = %d' % (customer.customer_id, listing.listing_id)))
#
#
#    @staticmethod
#    def find_favorites_by_customer(customer):
#        return Session.query(Listing)\
#            .join((ListingFavorite, ListingFavorite.listing_id == Listing.listing_id))\
#            .filter(and_(ListingFavorite.customer_id == customer.customer_id,
#                         ListingFavorite.delete_dt == None))
#
#
#class ListingMessage(ORMBase, BaseModel):
#    __tablename__ = 'pvs_listing_message'
#    __pk__ = 'listing_message_id'
#
#    listing_message_id = Column(Integer, primary_key = True)
#    listing_id = Column(Integer, ForeignKey('pvs_listing.listing_id'))
#    customer_id = Column(Integer, ForeignKey('crm_customer.customer_id'))
#    company_id = Column(Integer, ForeignKey('crm_company.company_id'))
#    parent_id = Column(Integer, ForeignKey('pvs_listing.listing_id'))
#    subject = Column(String(500))
#    message = Column(Text)
#    responder_email = Column(String(50)) # the guy responding to the listing
#    to_email = Column(String(50)) # the guy its to.  might be either.
#    from_email = Column(String(50)) # the guy sending the email.  might be either.
#    from_latitude = Column(Float)
#    from_longitude = Column(Float)
#    from_ip = Column(String(15))
#    create_dt = Column(DateTime, server_default = text('now()'))
#    delete_dt = Column(DateTime)
#    sent_dt = Column(DateTime)
#    status_id = Column(Integer, ForeignKey('core_status.status_id'))
#
#    customer = relation('Customer')
#    company = relation('Company')
#    status = relation('Status')
#
#
#    @property
#    def responder_key(self):
#        """ KB: [2011-06-29]: Gotta figure out how to do this in python so it works with PSQL md5 function indices. """
#        return db.get_value("select md5('%s')" % self.responder_email)
#
#
#    @property
#    def customer_key(self):
#        """ KB: [2011-06-29]: Gotta figure out how to do this in python so it works with PSQL md5 function indices. """
#        return db.get_value("select md5('%s')" % self.customer_id)
#
#
#    @property
#    def to_responder(self):
#        return self.responder_email == self.to_email
#
#
#    @property
#    def to_customer(self):
#        return not self.to_responder
#
#
#    @staticmethod
#    def validate_responder(listing, in_reply_to, responder_key):
#        return db.get_value("""select count(0) from pvs_listing_message
#                              where listing_id = {lid} and listing_message_id = {lmid}
#                              and md5(responder_email) = '{rkey}'""".format(lid=listing.listing_id,
#                                                                            lmid=in_reply_to.listing_message_id,
#                                                                            rkey=responder_key))
#
#
#    @staticmethod
#    def validate_customer(listing, in_reply_to, customer_key):
#        return db.get_value("""select count(0) from pvs_listing_message
#                              where listing_id = {lid} and listing_message_id = {lmid}
#                              and md5(text(customer_id)) = '{ckey}'""".format(lid=listing.listing_id,
#                                                                        lmid=in_reply_to.listing_message_id,
#                                                                        ckey=customer_key))
#
#
#    @staticmethod
#    def find_by_listing(listing):
#        return Session.query(ListingMessage).filter(and_(ListingMessage.delete_dt == None,
#                                                         #ListingMessage.sent_dt == None,
#                                                         ListingMessage.listing_id == listing.listing_id))\
#                                                         .order_by(ListingMessage.listing_message_id.desc())\
#                                                         .all()
#
#
#    @staticmethod
#    def find_count_by_email_and_listing(email, listing):
#        return Session.query(ListingMessage).filter(and_(ListingMessage.responder_email == email.lower(),
#                                                         ListingMessage.listing_id == listing.listing_id)).count()
#
#
#    @staticmethod
#    def find_by_customer(customer):
#        return Session.query(ListingMessage)\
#            .filter(and_(ListingMessage.customer == customer,
#                         ListingMessage.delete_dt == None))\
#                         .order_by(ListingMessage.create_dt.asc()).all()
#
#
#    @property
#    def children(self):
#        return Session.query(ListingMessage)\
#            .filter(and_(ListingMessage.parent_id == self.listing_message_id,
#                         ListingMessage.delete_dt==None))\
#                         .order_by(ListingMessage.create_dt.asc()).all()
#
#
#    @property
#    def parent(self):
#        if self.parent_id:
#            return ListingMessage(self.parent_id)
#
