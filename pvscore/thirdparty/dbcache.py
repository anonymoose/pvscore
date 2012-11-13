#pylint: disable-msg=W0212,W0231,C0103,W0107,E1101
"""
KB: [2011-02-07]: This is lifted directly from the SQLAlchemy examples.  Props to them.

Represent persistence structures which allow the usage of
Beaker caching with SQLAlchemy.

The three new concepts introduced here are:

 * CachingQuery - a Query subclass that caches and
   retrieves results in/from Beaker.
 * FromCache - a query option that establishes caching
   parameters on a Query
 * RelationshipCache - a variant of FromCache which is specific
   to a query invoked during a lazy load.
 * _params_from_query - extracts value parameters from
   a Query.

The rest of what's here are standard SQLAlchemy and
Beaker constructs.

"""
import time
from beaker import cache
from sqlalchemy.orm.interfaces import MapperOption
from sqlalchemy.orm.query import Query
from sqlalchemy.sql import visitors
import pvscore.config as config
#105-106, 120, 128-129, 153-154, 210-212, 223-229, 243-244, 256-269, 293
class CachingQuery(Query):
    """A Query subclass which optionally loads full results from a Beaker
    cache region.

    The CachingQuery stores additional state that allows it to consult
    a Beaker cache before accessing the database:

    * A "region", which is a cache region argument passed to a
      Beaker CacheManager, specifies a particular cache configuration
      (including backend implementation, expiration times, etc.)
    * A "namespace", which is a qualifying name that identifies a
      group of keys within the cache.  A query that filters on a name
      might use the name "by_name", a query that filters on a date range
      to a joined table might use the name "related_date_range".

    When the above state is present, a Beaker cache is retrieved.

    The "namespace" name is first concatenated with
    a string composed of the individual entities and columns the Query
    requests, i.e. such as ``Query(User.id, User.name)``.

    The Beaker cache is then loaded from the cache manager based
    on the region and composed namespace.  The key within the cache
    itself is then constructed against the bind parameters specified
    by this query, which are usually literals defined in the
    WHERE clause.

    The FromCache and RelationshipCache mapper options below represent
    the "public" method of configuring this state upon the CachingQuery.

    """

    def __init__(self, manager, *args, **kw):
        self.cache_manager = manager
        Query.__init__(self, *args, **kw)

    def __iter__(self):
        """override __iter__ to pull results from Beaker
           if particular attributes have been configured.

           Note that this approach does *not* detach the loaded objects from
           the current session. If the cache backend is an in-process cache
           (like "memory") and lives beyond the scope of the current session's
           transaction, those objects may be expired. The method here can be
           modified to first expunge() each loaded item from the current
           session before returning the list of items, so that the items
           in the cache are not the same ones in the current Session.

        """
        if hasattr(self, '_cache_parameters'):
            return self.get_value(createfunc=lambda: list(Query.__iter__(self)))
        else:
            return Query.__iter__(self)

    def invalidate(self):
        """Invalidate the value represented by this Query."""
        cache_, cache_key = _get_cache_parameters(self)
        #cache.clear()
        cache_.remove(cache_key)

    def get_value(self, merge=True, createfunc=None):
        """Return the value from the cache for this query.

        Raise KeyError if no value present and no
        createfunc specified.

        """
        cache_, cache_key = _get_cache_parameters(self)
        ret = cache_.get_value(cache_key, createfunc=createfunc)
        if merge:
            ret = self.merge_result(ret, load=False)
        return ret

    # def set_value(self, value):
    #     """Set the value in the cache for this query."""
    #     cache_, cache_key = _get_cache_parameters(self)
    #     cache_.put(cache_key, value)

def query_callable(manager):
    def query(*arg, **kw):
        return CachingQuery(manager, *arg, **kw)
    return query

def _get_cache_parameters(query):
    """For a query with cache_region and cache_namespace configured,
    return the correspoinding Cache instance and cache key, based
    on this query's current criterion and parameter values.

    """
    assert hasattr(query, '_cache_parameters')
    #raise ValueError("This Query does not have caching parameters configured.")

    region, namespace, cache_key = query._cache_parameters

    namespace = _namespace_from_query(namespace, query)

    if cache_key is None:
        args = _params_from_query(query)
        cache_key = " ".join([str(x) for x in args])

    # get cache
    cache_ = query.cache_manager.get_cache_region(namespace, region)

    # optional - hash the cache_key too for consistent length
    # import uuid
    # cache_key= str(uuid.uuid5(uuid.NAMESPACE_DNS, cache_key))

    return cache_, cache_key

def _namespace_from_query(namespace, query):
    # cache namespace - the token handed in by the
    # option + class we're querying against
    namespace = " ".join([namespace] + [str(x) for x in query._entities])

    # memcached wants this
    namespace = namespace.replace(' ', '_')

    return namespace

def _set_cache_parameters(query, region, namespace, cache_key):

    assert not hasattr(query, '_cache_parameters')
    #region, namespace, cache_key = query._cache_parameters
    #    raise ValueError("This query is already configured "
    #                    "for region %r namespace %r" %
    #                    (region, namespace)
    #                )
    query._cache_parameters = region, namespace, cache_key

class FromCache(MapperOption):
    """Specifies that a Query should load results from a cache."""
    propagate_to_loaders = False

    def __init__(self, namespace, cache_key=None, region='default'):
        """Construct a new FromCache.

        :param region: the cache region.  Should be a
        region configured in the Beaker CacheManager.

        :param namespace: the cache namespace.  Should
        be a name uniquely describing the target Query's
        lexical structure.

        :param cache_key: optional.  A string cache key
        that will serve as the key to the query.   Use this
        if your query has a huge amount of parameters (such
        as when using in_()) which correspond more simply to
        some other identifier.

        """
        self.region = region
        self.namespace = namespace
        self.cache_key = str(cache_key)

    def process_query(self, query):
        """Process a Query during normal loading operation."""
        _set_cache_parameters(query, self.region, self.namespace, self.cache_key)

# class RelationshipCache(MapperOption):
#     """Specifies that a Query as called within a "lazy load"
#        should load results from a cache."""

#     propagate_to_loaders = True

#     def __init__(self, namespace, attribute, region='default'):
#         """Construct a new RelationshipCache.

#         :param region: the cache region.  Should be a
#         region configured in the Beaker CacheManager.

#         :param namespace: the cache namespace.  Should
#         be a name uniquely describing the target Query's
#         lexical structure.

#         :param attribute: A Class.attribute which
#         indicates a particular class relationship() whose
#         lazy loader should be pulled from the cache.

#         """
#         self.region = region
#         self.namespace = namespace
#         self._relationship_options = {
#             ( attribute.property.parent.class_, attribute.property.key ) : self
#         }

#     def process_query_conditionally(self, query):
#         """Process a Query that is used within a lazy loader.

#         (the process_query_conditionally() method is a SQLAlchemy
#         hook invoked only within lazyload.)

#         """
#         if query._current_path:
#             mapper, key = query._current_path[-2:]

#             for cls in mapper.class_.__mro__:
#                 if (cls, key) in self._relationship_options:
#                     relationship_option = self._relationship_options[(cls, key)]
#                     _set_cache_parameters(
#                             query,
#                             relationship_option.region,
#                             relationship_option.namespace,
#                             None)

#     def and_(self, option):
#         """Chain another RelationshipCache option to this one.

#         While many RelationshipCache objects can be specified on a single
#         Query separately, chaining them together allows for a more efficient
#         lookup during load.

#         """
#         self._relationship_options.update(option._relationship_options)
#         return self


def _params_from_query(query):
    """Pull the bind parameter values from a query.

    This takes into account any scalar attribute bindparam set up.

    E.g. params_from_query(query.filter(Cls.foo==5).filter(Cls.bar==7)))
    would return [5, 7].

    """
    vals = []
    def visit_bindparam(bind):
        value = query._params.get(bind.key, bind.value)

        # lazyloader may dig a callable in here, intended
        # to late-evaluate params after autoflush is called.
        # convert to a scalar value.
        if callable(value):
            value = value()

        vals.append(value)
    if query._criterion is not None:
        visitors.traverse(query._criterion, {}, {'bindparam':visit_bindparam})
    return vals


# Beaker CacheManager.  A home base for cache configurations.
cache_manager = cache.CacheManager()

def init_cache_manager():
    ctype = config.settings['cache.type']
    if 'file' == ctype:
        cache_manager.regions['default'] = {
            # using type 'file' to illustrate
            # serialized persistence.  In reality,
            # use memcached.   Other backends
            # are much, much slower.
            'type':config.settings['cache.type'],
            'data_dir':config.settings['cache.data_dir'],
            'expire':86400,
            # set start_time to current time
            # to re-cache everything
            # upon application startup
            'start_time':time.time()
            }
        pass
    else:
        cache_manager.regions['default'] = {
            # using type 'file' to illustrate
            # serialized persistence.  In reality,
            # use memcached.   Other backends
            # are much, much slower.
            'type':config.settings['cache.type'],
            'url':config.settings['cache.url'],
            'lock_dir':config.settings['cache.lock_dir'],
            'expire':86400,
            # set start_time to current time
            # to re-cache everything
            # upon application startup
            'start_time':time.time()
            }

def invalidate(obj, region, cache_key=None):
    """ KB: [2011-02-07]:
    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Product.find_all', BaseModel.get_enterprise_id())
        invalidate(self, 'ProductChild.find_children', self.product_id)
        if kwargs and 'campaign_id' in kwargs:
            campaign_id = kwargs['campaign_id']
            invalidate(self, 'Product.Campaign_Featured', campaign_id)
            invalidate(self, 'Product.Campaign_Specials', campaign_id)
            invalidate(self, 'Product.Campaign', campaign_id)
    """
    from pvscore.model.meta import Session
    Session.query(obj.__class__).options(FromCache(region, cache_key)).invalidate()

