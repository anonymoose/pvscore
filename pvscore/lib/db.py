#pylint: disable-msg=E1101
import logging
from pvscore.model.meta import Session
from pvscore.lib.util import DataObj

log = logging.getLogger(__name__)

# def count(tbl, where=''):
#     return Session.bind.execute('select count(0) c from %s %s' % (tbl, where)).fetchone()[0]


# def save(obj):
#     Session.add(obj)
#     return True


# def commit():
#     Session.commit()
#     return True


# def execute_raw(sql):
#     Session.bind.execute(sql)


# def get_object_list(cls, sql):
#     return Session.query(cls).from_statement(sql).all()


# def get_object(cls, sql):
#     return Session.query(cls).from_statement(sql).one()


# def get_first(sql, **kwargs):
#     val = Session.bind.execute(sql, **kwargs).fetchall()
#     if val and len(val) > 0:
#         return val[0]


def get_list(sql, **kwargs):
    return Session.bind.execute(sql, **kwargs).fetchall()


# def get_column(sql, **kwargs):
#     return [c[0] for c in Session.bind.execute(sql, **kwargs).fetchall()]


def get_result_set(cols, sql, **kwargs):
    results = []
    for row in get_list(sql, **kwargs):
        obj = {}
        for i in range(len(cols)):
            obj[cols[i]] = row[i]
        results.append(DataObj(obj))
    return results


def get_result_dict(cols, sql, **kwargs):
    results = []
    for row in get_list(sql, **kwargs):
        obj = {}
        for i in range(len(cols)):
            obj[cols[i]] = row[i]
        results.append(obj)
    return results


def get_value(sql, **kwargs):
    ret = Session.bind.execute(sql, **kwargs).fetchone()
    if ret:
        return ret[0]


# def get_row(sql, **kwargs):
#     return Session.bind.execute(sql, **kwargs).fetchone()


def get_value_list(cls, col, sql):
    objs = Session.query(cls).from_statement(sql).all()
    return [getattr(o, col) for o in objs]


def get_raw_value_list(val, sql):
    tuples = Session.query(val).from_statement(sql).all()
    ret = []
    for tup in tuples:
        ret.append(tup[0])
    return ret


def clean(val):
    return val.replace("'", "''")
#    if val:
#        return val.replace('%', '').replace
