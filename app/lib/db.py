import pdb
import logging
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.orm import scoped_session, sessionmaker, relation, backref
from sqlalchemy.types import Integer, String, Date, Numeric, Text
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5
from app.model.meta import Session
from sqlalchemy.ext.sqlsoup import SqlSoup
from app.lib.util import DataObj

log = logging.getLogger(__name__)

"""
KB: [2010-08-26]: Simple layer when you are just quickly prototyping stuff against the DB.
http://www.sqlalchemy.org/trac/wiki/SqlSoup
"""

""" KB: [2010-08-26]: Must be called first. """
def init(): 
    pass

def count(tbl, where=''):
    return Session.bind.execute('select count(0) c from %s %s' % (tbl, where)).fetchone()[0]

def save(o):
    Session.add(o)
    return True

def commit():
    Session.commit()
    return True

def execute_raw(sql):
    Session.bind.execute(sql)

def get_object_list(cls, sql):
    return Session.query(cls).from_statement(sql).all()

def get_object(cls, sql):
    return Session.query(cls).from_statement(sql).one()

def get_first(sql, **kwargs):
    v = Session.bind.execute(sql, **kwargs).fetchall()
    if v and len(v) > 0: return v[0]

def get_list(sql, **kwargs):
    return Session.bind.execute(sql, **kwargs).fetchall()

def get_column(sql, **kwargs):
    return [c[0] for c in Session.bind.execute(sql, **kwargs).fetchall()]

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

def get_row(sql, **kwargs):
    return Session.bind.execute(sql, **kwargs).fetchone()

def get_value_list(cls, col, sql):
    objs = Session.query(cls).from_statement(sql).all()
    return [getattr(o, col) for o in objs]

def get_raw_value_list(val, sql):
    tuples = Session.query(val).from_statement(sql).all()
    ret = []
    for t in tuples:
        ret.append(t[0])
    return ret

def clean(val):
    return val.replace("'", "''")
#    if val:
#        return val.replace('%', '').replace
