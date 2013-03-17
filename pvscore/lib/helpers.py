import random
from webhelpers.html import literal
from webhelpers.html.tags import * #pylint: disable-msg=W0614,W0401,W0602,W0622
import pvscore.lib.util as util
import unicodedata


def nvl(val, default=''):
    if val == '' or val == None or val == 'None':
        return default
    return val


def onvl(obj, attr, default=''):
    """ KB: [2012-10-18]: NVL for objects "object nvl" """
    if obj and hasattr(obj, attr):
        return getattr(obj, attr)
    return default


def is_crm_logged_in(request):
    return ('crm_logged_in' in request.session and request.session['crm_logged_in'] == True)


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


def country_select_list(selected_country=None):
    return util.country_select_list(selected_country)


def is_notrack(request):
    """ KB: [2013-03-04]: See pvscore/controllers/cms/site:notrack() """
    return ('pvs_notrack' in request.session and request.session['pvs_notrack'] == 'notrack')\
        or ('pvs_notrack' in request.cookies.keys() and request.cookies['pvs_notrack'] == 'notrack')


def add_this_buttons_small(request, style=None):
    site = request.ctx.site
    if site and site.add_this_id:
        return literal("""
<!-- AddThis Button BEGIN -->
<div class="addthis_toolbox addthis_default_style" style="{style}">
<a class="addthis_button_pinterest"></a>
<a class="addthis_button_facebook"></a>
<a class="addthis_button_twitter"></a>
<a class="addthis_button_email"></a>
<span class="addthis_separator">|</span>
<a href="https://www.addthis.com/bookmark.php?v=250&amp;pubid={add_this_id}" class="addthis_button_compact">Share</a>
</div>
<script type="text/javascript">var addthis_config = {{ "data_track_clickback":true }};</script>
<script type="text/javascript" src="https://s7.addthis.com/js/250/addthis_widget.js#pubid={add_this_id}"></script>
<!-- AddThis Button END -->
                           """.format(add_this_id=site.add_this_id, style=style))
        

def add_this_buttons_large(request, style=None):
    site = request.ctx.site
    if site and site.add_this_id:
        return literal("""
<!-- AddThis Button BEGIN -->
<div class="addthis_toolbox addthis_default_style addthis_32x32_style" style="{style}">
<a class="addthis_button_pinterest"></a>
<a class="addthis_button_facebook"></a>
<a class="addthis_button_twitter"></a>
<a class="addthis_button_email"></a>
<a class="addthis_button_compact"></a>
<a class="addthis_counter addthis_bubble_style"></a>
</div>
<script type="text/javascript">var addthis_config = {{ "data_track_addressbar":true }};</script>
<script type="text/javascript" src="https://s7.addthis.com/js/300/addthis_widget.js#pubid={add_this_id}"></script>
<!-- AddThis Button END -->
                           """.format(add_this_id=site.add_this_id, style=style))
    

def google_analytics(request=None, site=None, script_tags=True):  #pragma: no cover
    if not site:
        site = request.ctx.site
    if site and site.google_analytics_id and is_production() and not is_notrack(request):
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


def eyefoundit_analytics(request=None, site=None): #pragma: no cover
    if not site:
        site = request.ctx.site
    if site and site.eyefoundit_analytics_id and is_production() and not is_notrack(request):
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


def clean(string):
    return util.clean(string)


def chkbox(ident, **kwargs):
    # we wrap this so that bootstrap can format our checkboxes properly
    hlp = ''
    if 'help' in kwargs:
        hlp = kwargs['help']
        del kwargs['help']
    label = ''
    if 'label' in kwargs:
        label = kwargs['label']
        del kwargs['label']
    return literal('<label class="checkbox">{chk}{label} {hlp}</label>'.format(chk=checkbox(ident, **kwargs),
                                                                               label=label,
                                                                               hlp=hlp))

def help(message, title_=''):  #pylint: disable-msg=W0622
    return literal('<a style="cursor:pointer;" data-toggle="popover" title="" data-content="%s" data-original-title="%s" class="pvs-help"><i class="icon-question-sign"></i></a>' % (message, title_))


def rnd():
    return random.random()

    

# def flt(dbl):
#     return money(dbl)


#def request_ip():
#    from pylons import request
#    return request.headers['X-Real-Ip']


#
# KB: [2013-03-04]: Functions for managing Aloha self edit capability in the site.
#
def aloha_header(request):
    #return ""
    if is_crm_logged_in(request):
        # <script src="/static/js/aloha/v0.23/aloha/lib/vendor/jquery-1.7.2.js"></script>
        # <script src="/static/js/aloha/v0.23/aloha/lib/require.js"></script>

# <script>
# Aloha = window.Aloha || {};
# Aloha.settings = Aloha.settings || {};
# // Restore the global $ and jQuery variables of your project's jQuery
# Aloha.settings.jQuery = window.jQuery.noConflict(true);
# </script>


        return literal("""
        <link rel="stylesheet" href="/static/js/aloha/v0.23/aloha/css/aloha.css" type="text/css">
        <script src="/static/js/aloha/v0.23/aloha/lib/aloha-full.js"
                data-aloha-plugins="common/ui,
common/image,
common/format,
common/highlighteditables,
common/table,
common/list,
common/undo,
common/paste,
common/commands,
common/link,
common/align"></script>
        <script src="/static/crm/js/pvs-aloha.js" type="text/javascript"></script>
        """)
    return ''


def aloha_footer(request):
    #return ""
    if is_crm_logged_in(request):
        return literal(""" """)
    return ""


def aloha_editable_attribute(request, obj, attr):
    val = getattr(obj, attr, '')
    pk_id = getattr(obj, obj.__pk__, '')
    if is_crm_logged_in(request):
        editable_id = '%s%s' % (obj.__pk__, attr)
        val = unicodedata.normalize('NFKD', val).encode('ascii','ignore') if val else ''
        return literal("""
                <div id="editable_{editable_id}">
                    {val}
                </div>
                <input type="hidden" id="editable_{editable_id}_type" value="attribute"/>
                <input type="hidden" id="editable_{editable_id}_objtype" value="{objtype}"/>
                <input type="hidden" id="editable_{editable_id}_module" value="{module}"/>
                <input type="hidden" id="editable_{editable_id}_attr" value="{attr}"/>
                <input type="hidden" id="editable_{editable_id}_pk_id" value="{pk_id}"/>
                <script type="text/javascript">
                    Aloha.ready( function() {{
                        Aloha.jQuery('#editable_{editable_id}').aloha();
                        Aloha.bind('aloha-editable-deactivated', pvs_aloha_onsave);
                    }} );
                </script>""".format(editable_id=editable_id,
                                    pk_id=pk_id,
                                    module=obj.__module__,
                                    attr=attr,
                                    objtype=obj.__class__.__name__,
                                    val=literal(str(val))))
    else:
        return literal(val)


def aloha_editable_content(request, content_name):
    from pvscore.model.cms.content import Content
    site = request.ctx.site
    content = Content.find_by_name(site, content_name, False)
    if content:
        editable_id = content_name.replace('.', '_')
        html = literal("""
                <div id="editable_{editable_id}">
                    {val}
                </div>
                <input type="hidden" id="editable_{editable_id}_type" value="content"/>
                <input type="hidden" id="editable_{editable_id}_name" value="{name}"/>
                <input type="hidden" id="editable_{editable_id}_content_id" value="{content_id}"/>
                <script type="text/javascript">
                    Aloha.ready( function() {{
                        Aloha.jQuery('#editable_{editable_id}').aloha();
                        Aloha.bind('aloha-editable-deactivated', pvs_aloha_onsave);
                    }} );
                </script>""".format(editable_id=editable_id,
                                    content_id=content.content_id,
                                    name=content_name,
                                    val=content.render(request=request) if content else ''))
    return html
                

def lightbox(imgsrc, caption=None, lbid=None, style=None):
    return literal("""
    <a href="#{lbid}" data-toggle="lightbox"><img src="{imgsrc}" style="{style}"/></a>
    <div id="{lbid}" class="lightbox hide fade"  tabindex="-1" role="dialog" aria-hidden="true">
      <div class='lightbox-header'>
        <button type="button" class="close" data-dismiss="lightbox" aria-hidden="true">&times;</button>
      </div>
      <div class='lightbox-content'>
        <img src="{imgsrc}"/>
        {caption}
      </div>
    </div>
    """.format(imgsrc=imgsrc, style=style, lbid=lbid,
               caption='<div class="lightbox-caption"><p>%s</p></div>' % caption if caption else ''))
