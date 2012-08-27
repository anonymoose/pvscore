import pdb, logging
import inspect, datetime, time, os, transaction, redis
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.orm import scoped_session, sessionmaker, relation, backref
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.types import Integer, String, Date, Numeric, Text
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5
import simplejson as json
import app.lib.util as util
import app.lib.dbcache as dbcache
from app.lib.dbcache import FromCache
from app.model import *
from zope.sqlalchemy import ZopeTransactionExtension


log = logging.getLogger(__name__)

__all__ = ['Base', 'Session', 'Redis']

#RedisPool = redis.ConnectionPool(host='localhost', port=6379, db=1)
#Redis = redis.Redis(connection_pool=RedisPool)


# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(
                sessionmaker(
                    expire_on_commit=False,
                    query_cls=dbcache.query_callable(dbcache.cache_manager),
                    extension=ZopeTransactionExtension('changed')  #http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/pylons/models.html
                                                                   #http://pypi.python.org/pypi/zope.sqlalchemy/
                    )
                )

# The declarative Base
ORMBase = declarative_base()

class BaseModel:
#    def __repr__(self):
#       return self.to_json()

    def to_dict(self, maxlevel=2, level=0):
        if level > maxlevel: return

        keys = [m for m in dir(self) if not m.startswith('_')
                and (isinstance(getattr(self, m), list)
                     or isinstance(getattr(self, m), int)
                     or isinstance(getattr(self, m), str)
                     or isinstance(getattr(self, m), unicode)
                     or isinstance(getattr(self, m), float)
                     or isinstance(getattr(self, m), datetime.date)
                     or hasattr(getattr(self, m), 'to_dict'))]
        data = {}
        for k in keys:
            v = getattr(self, k)
            if isinstance(v, list):
                data[k] = []
                for j in v:
                    if hasattr(j, 'to_dict'):
                        d = j.to_dict(maxlevel, level+1)
                        if d and len(d) > 0: data[k].append(d)
                    elif isinstance(j, datetime.date):
                        data[k] = str(j)
                    else:
                        data[k] = j
            else:
                if hasattr(v, 'to_dict'):
                    d = v.to_dict(maxlevel, level+1)
                    if d and len(d) > 0: data[k] = d
                elif isinstance(v, datetime.date):
                    data[k] = str(v)
                else:
                    data[k] = v
        return data

    def to_json(self, maxlevel=2):
        return json.dumps(self.to_dict(), maxlevel)

    @classmethod
    def load(cls, pk, cache=True):
        """ KB: [2010-08-13]: Pass the primary key, get back an object"""
        if pk is None or pk == '': return None
        try:
            if not cache:
                obj = Session.query(cls).filter("%s.%s = :val" % (cls.__tablename__, cls.__pk__)).params(val=pk).one()
            else:
                obj = Session.query(cls).options(FromCache('%s.load' % cls.__name__, pk)).filter("%s.%s = :val" % (cls.__tablename__, cls.__pk__)).params(val=pk).one()
            obj.post_load()
            return obj
        except Exception as e:
            raise e
        #return None

    @classmethod
    def load_ids(cls, pk_list):
        return Session.query(cls).from_statement("SELECT * FROM %s where %s in (%s)" \
                                                     % (cls.__tablename__, cls.__pk__, ','.join([str(pk) for pk in pk_list]))).all()

    """ KB: [2010-11-15]: Override this to get something called right after load. """
    def post_load(self):
        pass

    def expire(self):
        Session.expire(self)
        Session.flush()

    def expunge(self):
        Session.expunge(self)
        Session.flush()

    @classmethod
    def delete_all(cls, where=''):
        Session.execute('delete from %s %s' % (cls.__tablename__, where))

    def delete(self):
        # invalidate the single load cache from load() and tell the object to
        # invalidate itself.
        self._invalidate_self()
        try:
            self.invalidate_caches()
        except: pass

        Session.delete(self)

    def soft_delete(self):
        # If there is a delete_dt attribute, then set it to "now" and save it.
        self._invalidate_self()
        try:
            self.invalidate_caches()
            self.delete_dt = util.today()
            self.save()
            return True
        except:
            return False

    @classmethod
    def count(cls, where=''):
        ret = Session.query("c").from_statement("SELECT count(0) c FROM %s %s" % (cls.__tablename__, where)).one()
        return ret[0]

    def bind(self, dic, clear=False, prefix=None):
        """ KB: [2010-08-14]: dic is a paste MultiDict which behaves like a dictionary, but preserves order.
        don't try to bind anything on the object that starts with a '_' or if the pk has nothing in it.
        (If we tried to pass a '' instead of None for a numeric PK then it barfs.)
        """
        if clear:
            """ KB: [2010-09-15]: Checkboxes (booleans) get sent only when they are true.  Make sure that unchecked
            bools get set to false.  TODO: Should "clear" always be true?
            """
            for m in inspect.getmembers(type(self)):
                attr_name = m[0]
                attr = getattr(self, attr_name)
                if not attr_name.startswith('_') and not callable(attr):
                    if attr_name != self.__pk__:
                        if type(attr) == bool:  # and ('%s_%s' % (prefix, attr_name) if prefix else attr_name) in dic.keys():
                            try:
                                setattr(self, attr_name, False)
                            except: pass

        for k in dic.keys():
            attr_name = k.replace('%s_' % prefix if prefix else '', '')
            if hasattr(self, attr_name):
                attr = getattr(self, attr_name)
                if not attr_name.startswith('_') and not callable(attr):
                    if attr_name == self.__pk__:
                        if dic[k] is not None and dic[k] != '':
                            setattr(self, attr_name, dic[k])
                    else:
                        if dic[k] == '': dic[k] = None
                        setattr(self, attr_name, dic[k])

    def invalidate_caches(self, **kwargs):
        """ KB: [2011-02-07]: Override this in your data class to invalidate caches related to individual load objects and
        lists that this object may be contained in.
        """
        self._invalidate_self()

    def _invalidate_self(self):
        if self.__pk__:
            Session.query(self.__class__).options(FromCache('%s.load' % self.__class__.__name__,
                                                            getattr(self, self.__pk__))).invalidate()

    def save(self):
        # invalidate the single load cache from load() and tell the object to
        # invalidate itself.
        self._invalidate_self()
        try:
            self.invalidate_caches()
        except: pass

        Session.add(self)
        return True

    def flush(self):
        Session.flush()
        return True

    def doom(self):
        transaction.doom()
        return True


""" KB: [2011-11-01]: Base class for reports that can render a SQL statement to a google chart or whatver
"""
class BaseAnalytic:
    @property
    def columns(self): pass

    @property
    def query(self): pass

    def run(self):
        import app.lib.db as db
        self.results = db.get_result_set(self.columns, self.query)
        return self.results

    def col_max(self, colname, convert=float):
        seq = [convert(util.nvl(getattr(r, colname), 0)) for r in self.results if hasattr(r, colname)]
        return max(seq) if len(seq) else 0

    def col_min(self, colname, convert=float):
        seq = [convert(util.nvl(getattr(r, colname), 0)) for r in self.results if hasattr(r, colname)]
        return min(seq) if len(seq) else 0

    @property
    def numrows(self):
        return len(self.results)

""" KB: [2010-09-22]: Handling for SOAPLIB 0.8.1 """

#import soaplib.serializers.primitive # String, Integer, Array, DateTime, Float
#from soaplib.serializers.clazz import ClassSerializer, ClassSerializerMeta
#import inspect
#
#class SoapModelMeta(ClassSerializerMeta):
#    """ KB: [2010-09-22]: http://wiki.pylonshq.com/display/pylonscookbook/SOAP+Controller+with+Optio's+Soaplib+and+SQLAlchemy
#    What is recommended in the article is to separately declare the struct types and the models.
#    Instead, declare a small class that has a "__proxy_for" attribute of the model class in question.  This meta class
#    will populate everything that matters into the small class's "types" subclass so that all of the
#    soaplib magic works.
#    """
#    def __init__(cls, clsname, bases, dictionary):
#        '''
#        This initializes the class and ensures that there's a soap representation in types for each
#        member var that is a column.
#        '''
#        if not hasattr(cls,'types') or not hasattr(cls, '_%s__proxy_for' % clsname):
#            return
#
#        types = cls.types
#        proxy = getattr(cls, '_%s__proxy_for' % clsname)
#        members = dict(inspect.getmembers(proxy))
#        for k,v in members.items():
#            if not k.startswith('__') and not callable(v) and hasattr(v, 'property') and v.property.__class__.__name__ == 'ColumnProperty':
#                classname = v.property.columns[0].type.__class__.__name__
#                if classname == 'String' or classname == 'Text':
#                    setattr(types, k, soaplib.serializers.primitive.String)
#                elif classname == 'Integer':
#                    setattr(types, k, soaplib.serializers.primitive.Integer)
#                elif classname == 'Float':
#                    setattr(types, k, soaplib.serializers.primitive.Float)
#                elif classname == 'Boolean':
#                    setattr(types, k, soaplib.serializers.primitive.Boolean)
#                elif classname == 'Date':
#                    setattr(types, k, soaplib.serializers.primitive.DateTime)
#
#        ClassSerializerMeta.__init__(cls, clsname, bases, dictionary)
#
#class BaseApiModel(BaseModel, ClassSerializer):
#    __metaclass__ = SoapModelMeta
#
#    def map_to_proxy(self):
#        pass

