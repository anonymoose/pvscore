import random
from webhelpers.html import literal
from webhelpers.html.tags import * #pylint: disable-msg=W0614,W0401,W0602,W0622
import pvscore.lib.util as util


def nvl(val, default=''):
    if val == '' or val == None or val == 'None':
        return default
    return val


def onvl(obj, attr, default=''):
    """ KB: [2012-10-18]: NVL for objects "object nvl" """
    if obj and hasattr(obj, attr):
        return getattr(obj, attr)
    return default


def is_dialog(request):
    return (request.GET.get('dialog') == '1')


def is_api(request):
    return request.path.startswith('/api') or request.GET.get('api') == '1'


def money(dbl):
    if type(dbl) == float and round(dbl, 2) == -0.00:
        dbl = 0.00
    if dbl or type(dbl) == float:
        return '%.2f' % float(dbl)
    else: return ''


def state_select_list(selected_st=None):
    return util.state_select_list(selected_st)


def google_analytics(site, script_tags=True):
    if site and site.google_analytics_id and is_production():
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
    return ''


def eyefoundit_analytics(site):
    if site and site.eyefoundit_analytics_id and is_production():
        return literal('''
    <!-- Piwik -->
<script type="text/javascript">
var pkBaseURL = (("https:" == document.location.protocol) ? "https://www.eyefound.it/" : "http://www.eyefound.it/");
document.write(unescape("%%3Cscript src='" + pkBaseURL + "stats/piwik.js' type='text/javascript'%%3E%%3C/script%%3E"));
</script><script type="text/javascript">
try {
var piwikTracker = Piwik.getTracker(pkBaseURL + "stats/piwik.php", %s);
piwikTracker.trackPageView();
piwikTracker.enableLinkTracking();
} catch( err ) {}
</script><noscript><p><img src="https://www.eyefound.it/stats/piwik.php?idsite=%s" style="border:0" alt="" /></p></noscript>
<!-- End Piwik Tracking Code -->
    ''' % (site.eyefoundit_analytics_id, site.eyefoundit_analytics_id))
    return ''


def is_today(dat):
    return util.format_date(dat) == util.str_today()


def is_production():
    return util.is_production()


def this_year():
    return util.this_year()


def date_time(d8e, fmt="%Y-%m-%d %H:%M:%S"):
    if d8e == '' or d8e == None:
        return ''
    return d8e.strftime(fmt)


def date_(d8e, fmt="%Y-%m-%d"):
    if d8e == '' or d8e == None:
        return ''
    return d8e.strftime(fmt)


def format_date(d8e, fmt="%Y-%m-%d"):
    if d8e == '' or d8e == None:
        return ''
    return d8e.strftime(fmt)


def words_date_time(d8e):
    if d8e == '' or d8e == None:
        return ''
    return d8e.strftime("%B %d, %Y at %I:%M %p")


def str_today():
    return util.str_today()

def slash_date(d8e):
    if d8e == '' or d8e == None:
        return ''
    return d8e.strftime("%m/%d/%Y")


def words_date(d8e):
    if d8e == '' or d8e == None:
        return ''
    return d8e.strftime("%B %d, %Y")


def javascript_link_ex(url, request):
    return javascript_link(url+'?rnd='+str(request.session.get('_creation_time', random.random())))


def stylesheet_link_ex(url, request):
    return stylesheet_link(url+'?rnd='+str(request.session.get('_creation_time', random.random())))


def nl2br(val):
    return val.replace('\n','<br>\n')


def get(obj, attr, default=''):
    if not obj or not hasattr(obj, attr):
        return default
    return getattr(obj, attr)

def chkbox(ident, **kwargs):
    # we wrap this so that bootstrap can format our checkboxes properly
    return literal('<label class="checkbox">%s</label>' % checkbox(ident, **kwargs))


# def flt(dbl):
#     return money(dbl)


#def request_ip():
#    from pylons import request
#    return request.headers['X-Real-Ip']


