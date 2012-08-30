"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
import pdb

import datetime, os, errno
from webhelpers.html import literal
from webhelpers.html.tags import *
import app.lib.util as util
import random as rnd

def button(id, display, **kwargs):
    append = ''
    for k in kwargs.keys():
        append = '%s %s="%s"' % (append, k if k != 'class_' else 'class', kwargs.get(k))
    return literal('<input id="%s" name="%s" type="button" value="%s" %s>' % (id, id, display, append))

#def hidden(id, value, **kwargs):
#    append = ''
#    for k in kwargs.keys():
#        append = '%s %s="%s"' % (append, k, kwargs.get(k))
#    return literal('<input id="%s" name="%s" type="hidden" value="%s" %s>' % (id, id, value, append))
#

def nvl(s, default=''):
    if s == '' or s == None or s == 'None':
        return default;
    return s;

def is_dialog(request):
    return (request.GET.get('dialog') == '1')

def is_api(request):
    return request.path.startswith('/api') or request.GET.get('api') == '1'

def is_mobile():
    return MobileDetector.is_mobile(request)

def is_logged_in_site():
    return ('customer_id' in session and session['customer_id'] and 'customer_logged_in' in session and session['customer_logged_in'] == True)

def money(dbl):
    if type(dbl) == float and round(dbl, 2) == -0.00: dbl = 0.00
    if dbl or type(dbl) == float:
        return '%.2f' % float(dbl)
    else: return ''

def flt(dbl):
    return money(dbl)

def google_analytics(site, script_tags=True, version=None):
    if not site: return ''
    if site.google_analytics_id:
        return literal("""
    {st_start}
      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', '{googid}']);
      _gaq.push(['_trackPageview']);

      (function() {{
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      }})();
    {st_end}
    """.format(st_start='<script type="text/javascript">' if script_tags else '',
               st_end = '</script>' if script_tags else '',
               googid=site.google_analytics_id))
    else:
        return ''


paypal_url = 'https://www.paypal.com/cgi-bin/webscr'

def last_flash():
    flashes = flash.pop_messages()
    if flashes:
        return flashes.pop()
    return ''

def date_time(d, fmt="%Y-%m-%d %H:%M:%S"):
    if d == '' or d == None:
        return ''
    return d.strftime(fmt)

def date_(d, fmt="%Y-%m-%d"):
    if d == '' or d == None:
        return ''
    return d.strftime(fmt)

def format_date(d, fmt="%Y-%m-%d"):
    if d == '' or d == None:
        return ''
    return d.strftime(fmt)

def words_date_time(d):
    if d == '' or d == None:
        return ''
    return d.strftime("%B %d, %Y at %I:%M %p")

def slash_date(d):
    if d == '' or d == None:
        return ''
    return d.strftime("%m/%d/%Y")

def words_date(d):
    if d == '' or d == None:
        return ''
    return d.strftime("%B %d, %Y")

def is_production():
    return util.is_production()

def request_ip():
    from pylons import request
    return request.headers['X-Real-Ip']

""" KB: [2011-08-01]: If you are on /About and you really want to use content from /Home, do it like so...
${h.duplicate_content(c.site, 'Home', 'left')}
"""
def duplicate_content(site, pagename, content_name, **kwargs):
    p = Page.find_by_name(site, pagename)
    cnt = Content.find_by_name_and_type(p, content_name, 'html')
    if cnt:
        return cnt.render(**kwargs)
    return ''

def javascript_link_ex(url, request):
    return javascript_link(url+'?rnd='+str(session['_creation_time']))

def stylesheet_link_ex(url, request):
    return stylesheet_link(url+'?rnd='+str(session['_creation_time']))

def nl2br(s):
    return s.replace('\n','<br>\n')

def get(o, attr, default=''):
    if not o: return default
    return getattr(o, attr, default)

