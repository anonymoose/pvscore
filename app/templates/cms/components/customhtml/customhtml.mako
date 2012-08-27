## inherit from super_component so you get frameworky functionality.
<%inherit file="../super_component.mako"/>\

<%!
from app.lib.component import BaseComponent
from app.model.cms.page import Page
import re, pdb

class CustomHtmlComponent(BaseComponent):
    def __init__(self, component_type, content=None):
        self.component_type = component_type
        self.content = content
        self.initial_id = BaseComponent.generate_initial_id()
%>

<%
component = CustomHtmlComponent(c.content_type, c.content if hasattr(c, 'content') else None)
self.render(component)
%>

<%def name="render_create(component)">
    <div id="cmp_customhtml_div_${component.initial_id}" 
         initial_id="${component.initial_id}" 
         style="text-align:center;"
         onclick="cmp_customhtml_edit(this)">
    <br><br><br>
    Click Here for HTML
    <br><br><br>
    </div>
</%def>

<%def name="render_edit(component)">
<%
    data = component.content.data
    html = component.content.data_to_json()
%>
    <div id="cmp_customhtml_div_${component.content.content_id}" 
         onclick="cmp_customhtml_edit(this, ${component.content.content_id})"
         initial_id="${component.content.content_id}" 
         style="text-align:center;"
         class="cms-dbstored">
      ${component.dynamic_render(html['html'])}
    </div>
</%def>

<%def name="render_edit_js(component)">

/* KB: [2010-11-19]: This is the data structure that is stored in cms_content.data */
var cmp_customhtml_data = {
    id: null,
    html: null
};

/* KB: [2010-11-19]: If the component is new (just dragged) then this will be null.  otherwise
it will contain cms_content.content_id of the thing we are working with. */
var cmp_customhtml_existing_id = null;

/* KB: [2010-11-19]: Called when the element is clicked.  Be ready to edit existing and edit new.
   Since there is no DB ID initially, we get one from the system via Picture.initial_id.  This ID will
   be replaced with the one from the database after it is persisted.
 */
cmp_customhtml_edit = function(placeholder, existing_id) {
    cmp_customhtml_existing_id = null;
    var initial_id = $(placeholder).attr('initial_id');
    cmp_customhtml_clear_tmp_data();
    pvs.dialog.display({url:pvs.ajax.api({root: '/cms/content/component/call/customhtml/show_edit_dialog'}),
                        title: 'Add HTML',
                        width:830, 
                        height:520,
                        after_display_impl:
                        function() {
                            if (existing_id) {
                                pvs.ajax.call(pvs.ajax.api({root: '/cms/content/show_data/'+existing_id}),
                                                             function(response) {
                                                                 cmp_customhtml_existing_id = existing_id;
                                                                 cmp_customhtml_data = pvs.json.decode(response);
                                                                 cmp_customhtml_data.id = existing_id;
                                                                 $('#cmp_customhtml_html').val(cmp_customhtml_data.html);
                                                                 cmp_customhtml_edit_update_txt('cmp_customhtml_div');
                                                                 cmp_customhtml_edit_update_vars();
                                                             });
                            }
                        },
                        on_before_close:
                        function() {
                            cmp_customhtml_data.id = initial_id;
                            cmp_customhtml_update_tmp_data();
                            return true;
                        },
                        on_ok: 
                        function() {
                            cmp_customhtml_data.id = initial_id;
                            cmp_customhtml_update_tmp_data();
                            cmp_customhtml_save();
                        }
                });
};

cmp_customhtml_edit_update = function(selector) {
    cmp_customhtml_clear_tmp_data(true);
    cmp_customhtml_update_tmp_data();
    cmp_customhtml_edit_update_txt(selector);
};

cmp_customhtml_clear_tmp_data = function(preserve_readonly) {
    if (!preserve_readonly) {
        cmp_customhtml_data.id = null;
    }
    cmp_customhtml_data.html = null;
};

cmp_customhtml_update_tmp_data = function() {
    cmp_customhtml_data.html = $_('#cmp_customhtml_html');
};

cmp_customhtml_edit_update_vars = function() {
    $('#cmp_customhtml_html').val(cmp_customhtml_data.html);
};

cmp_customhtml_edit_update_txt = function(selector) {
    var img_id = '#'+selector+'_'+cmp_customhtml_data.id;
    $(img_id).val(cmp_customhtml_data.html);
};

cmp_customhtml_save = function() {
    var arr = {};
    arr['data'] = pvs.json.encode(cmp_customhtml_data);
    pvs.ajax.post_array(pvs.ajax.api({root: '/cms/content/save/customhtml/'+$_('#site_id'), 
                                      content_id: cmp_customhtml_existing_id}),
                        function(response) {
                            var resp = pvs.json.decode(response);
                            if (resp.id) {
                                var orig_id = cmp_customhtml_data.id;
                                cmp_customhtml_data.id = resp.id;
                                if (orig_id != resp.id) {
                                    // this is the first save.
                                    $('#cmp_customhtml_div_'+orig_id).attr('id', 'cmp_customhtml_div_'+resp.id);
                                }
                                cmp_customhtml_edit_update_txt('cmp_customhtml_div');
                                $('#cmp_customhtml_div_'+cmp_customhtml_data.id).wrap('<div id="div_'+resp.id+'"></div>');
                                // re-render at the page level and tell the page that it should update its layout.
                                $('#div_'+resp.id).load(pvs.ajax.api({root: '/cms/content/render_edit/${component.component_type.type_id}/'+resp.id}), 
                                                        function(response) {
                                                            page_update_contents();
                                                        });
                            } else {
                                pvs.alert(response);
                            }
                        },
                        arr
                       );
};

</%def>

<%def name="render_view(component)">
<%
    data = component.content.data
    html = component.content.data_to_json()
%>
    <div style="text-align:center;">
      ${component.dynamic_render(html['html'])}
    </div>
</%def>

<%def name="render_view_js(component)">
</%def>

<%def name="render_view_css(component)">
</%def>

## public methods that are used for the implementation of the component but are
## not necessarily part of the generic API.
<%def name="show_edit_dialog(component)">
<table>
  <tr>
    <td colspan="2">
      <p>
        Type in HTML directly.
      </p>
    </td>
  </tr>
  <tr>
    <td colspan="2">
    ${h.textarea('cmp_customhtml_html', style="width: 795px; height: 350px;", class_='html_editor')}
    </td>
  </tr>
</table>
</%def>


