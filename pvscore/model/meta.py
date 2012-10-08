import logging
import inspect
#import transaction
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pvscore.lib.util as util
import pvscore.lib.dbcache as dbcache
from pvscore.lib.dbcache import FromCache
from zope.sqlalchemy import ZopeTransactionExtension  #pylint: disable-msg=E0611,F0401

log = logging.getLogger(__name__)

__all__ = ['Base', 'Session', 'Redis']
Session = scoped_session(          #pylint: disable-msg=C0103
                sessionmaker(
                    expire_on_commit=False,
                    query_cls=dbcache.query_callable(dbcache.cache_manager),
                    extension=ZopeTransactionExtension('changed')  #http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/pylons/models.html
                                                                   #http://pypi.python.org/pypi/zope.sqlalchemy/
                    )
                )

ORMBase = declarative_base()  #pylint: disable-msg=C0103

class BaseModel(object):
    __pk__ = ''
    __tablename__ = ''

    # def __init__(self):
    #     pass


    @classmethod
    def load(cls, pkey, cache=True):
        """ KB: [2010-08-13]: Pass the primary key, get back an object"""
        if pkey is None or pkey == '':
            return None

        if not cache:
            obj = Session.query(cls).filter("%s.%s = :val" % (cls.__tablename__, cls.__pk__)).params(val=pkey).first()    #pylint: disable-msg=E1101
        else:
            obj = Session.query(cls).options(FromCache('%s.load' % cls.__name__, pkey)).filter("%s.%s = :val" % (cls.__tablename__, cls.__pk__)).params(val=pkey).first()    #pylint: disable-msg=E1101
        if obj:
            obj.post_load()
        return obj


    # @classmethod
    # def load_ids(cls, pk_list):
    #     return Session.query(cls).from_statement("SELECT * FROM %s where %s in (%s)" % (cls.__tablename__, cls.__pk__, ','.join([str(pk) for pk in pk_list]))).all()    #pylint: disable-msg=E1101


    def post_load(self):
        pass


    # def expire(self):
    #     Session.expire(self)    #pylint: disable-msg=E1101
    #     Session.flush()    #pylint: disable-msg=E1101


    # def expunge(self):
    #     Session.expunge(self)    #pylint: disable-msg=E1101
    #     Session.flush()    #pylint: disable-msg=E1101


    # @classmethod
    # def delete_all(cls, where=''):
    #     Session.execute('delete from %s %s' % (cls.__tablename__, where))    #pylint: disable-msg=E1101


    def delete(self):
        # invalidate the single load cache from load() and tell the object to
        # invalidate itself.
        self.invalidate_self()
        #try:
        self.invalidate_caches()
        #except Exception as exc:   #pylint: disable-msg=W0703
        #    log.debug(exc)
        Session.delete(self)    #pylint: disable-msg=E1101


    def soft_delete(self):
        # If there is a delete_dt attribute, then set it to "now" and save it.
        self.invalidate_self()
        self.invalidate_caches()
        self.delete_dt = util.today()   #pylint: disable-msg=W0201
        self.save()
        return True


    # @classmethod
    # def count(cls, where=''):
    #     ret = Session.query("c").from_statement("SELECT count(0) c FROM %s %s" % (cls.__tablename__, where)).one()    #pylint: disable-msg=E1101
    #     return ret[0]


    def bind(self, dic, clear=False, prefix=None):     #pylint: disable-msg=R0912
        """ KB: [2010-08-14]: dic is a paste MultiDict which behaves like a dictionary, but preserves order.
        don't try to bind anything on the object that starts with a '_' or if the pk has nothing in it.
        (If we tried to pass a '' instead of None for a numeric PK then it barfs.)
        """
        if clear:
            # KB: [2010-09-15]: Checkboxes (booleans) get sent only when they are true.  Make sure that unchecked
            # bools get set to false.
            for mem in inspect.getmembers(type(self)):
                attr_name = mem[0]
                attr = getattr(self, attr_name)
                if not attr_name.startswith('_') and not callable(attr):
                    if attr_name != self.__pk__:
                        if type(attr) == bool:  # and ('%s_%s' % (prefix, attr_name) if prefix else attr_name) in dic.keys():
                            try:
                                setattr(self, attr_name, False)
                            except Exception as exc:   #pylint: disable-msg=W0703
                                log.debug(exc)
        for key in dic.keys():
            attr_name = key.replace('%s_' % prefix if prefix else '', '')
            if hasattr(self, attr_name):
                attr = getattr(self, attr_name)
                if not attr_name.startswith('_') and not callable(attr):
                    if attr_name == self.__pk__:
                        if dic[key] is not None and dic[key] != '':
                            setattr(self, attr_name, dic[key])
                    else:
                        if dic[key] == '':
                            dic[key] = None
                        setattr(self, attr_name, dic[key])


    def invalidate_caches(self, **kwargs):  #pylint: disable-msg=W0613
        """ KB: [2011-02-07]: Override this in your data class to invalidate caches related to individual load objects and
        lists that this object may be contained in.
        """
        self.invalidate_self()


    def invalidate_self(self):
        if self.__pk__:
            Session.query(self.__class__).options(FromCache('%s.load' % self.__class__.__name__,      #pylint: disable-msg=E1101
                                                            getattr(self, self.__pk__))).invalidate()


    def save(self):
        # invalidate the single load cache from load() and tell the object to
        # invalidate itself.
        self.invalidate_self()
        try:
            self.invalidate_caches()
        except Exception as exc:   #pylint: disable-msg=W0703
            log.debug(exc)
        Session.add(self)    #pylint: disable-msg=E1101
        return self


    def flush(self):
        Session.flush()    #pylint: disable-msg=E1101
        return self


    # def doom(self):
    #     transaction.doom()
    #     return True


    def clear_attributes(self):
        from pvscore.model.core.attribute import Attribute
        pkid = getattr(self, self.__pk__)
        if pkid:
            Attribute.clear_all(self.__class__.__name__, pkid)


    def set_attr(self, name, value):
        from pvscore.model.core.attribute import Attribute
        attr = Attribute.find(self.__class__.__name__, name)
        if not attr:
            attr = Attribute.create_new(self.__class__.__name__, name)
        attr.set(self, value)


    def get_attr(self, name):
        from pvscore.model.core.attribute import Attribute
        attr = Attribute.find(self.__class__.__name__, name)
        if attr:
            return attr.get(self)


    def get_attrs(self):
        from pvscore.model.core.attribute import Attribute        
        return Attribute.find_values(self)


# KB: [2011-11-01]: Base class for reports that can render a SQL statement to a google chart or whatver
class BaseAnalytic(object):
    def __init__(self):
        self.results = None


    @property
    def columns(self):
        pass


    @property
    def query(self):
        pass


    def run(self):
        import pvscore.lib.db as db
        self.results = db.get_result_set(self.columns, self.query)
        return self.results 


    def col_max(self, colname, convert=float):
        seq = [convert(util.nvl(getattr(r, colname), 0)) for r in self.results if hasattr(r, colname)]
        return max(seq) if len(seq) else 0


    # def col_min(self, colname, convert=float):
    #     seq = [convert(util.nvl(getattr(r, colname), 0)) for r in self.results if hasattr(r, colname)]
    #     return min(seq) if len(seq) else 0


    # @property
    # def numrows(self):
    #     return len(self.results)

