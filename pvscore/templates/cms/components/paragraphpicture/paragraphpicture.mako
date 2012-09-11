<%inherit file="../super_component.mako"/>\

<%!
from app.lib.component import BaseComponent
from app.model.cms.page import Page
import re, pdb

class ParagraphPictureComponent(BaseComponent):
    def __init__(self, component_type, content=None):
        self.component_type = component_type
        self.content = content
        self.initial_id = BaseComponent.generate_initial_id()
%>

<%
component = ParagraphPictureComponent(c.content_type, c.content if hasattr(c, 'content') else None)
self.render(component)
%>

<%def name="render_create(component)">
    <div id="cmp_paragraphpicture_div_${component.initial_id}" 
         initial_id="${component.initial_id}" 
         style="text-align:center; height: 170px;">
      <h2 style="text-align: left;" 
          class="cms-editable-text" 
          onclick="cmp_paragraphpicture_edit(this, ${component.initial_id}, false)"
          id="cmp_paragraphpicture_title_${component.initial_id}">
        Click Here to Edit
      </h2>
      <br>
      <span style="float: left; height: 0px; display:block;overflow:hidden;"></span>
      <span style="z-index: 10; float: left; position: relative; clear: left; margin-top: 0px;">
        <a>
          <img src="/cms/images/sample-image.jpg">
        </a>
        <div style="display: block; font-size: 90%; margin-top: -10px; margin-bottom: 10px; text-align: center;"></div>
      </span>
      <div style="text-align: left; display: block;" 
           class="cms-editable-text" 
           id="cmp_paragraphpicture_body_${component.initial_id}"
          onclick="cmp_paragraphpicture_edit(this, ${component.initial_id}, false)">
         This is the next line.</div><br>
    </div>
</%def>

<%def name="render_edit(component)">
<%
    data = component.content.data_to_json()
%>
    <div id="cmp_paragraphpicture_div_${component.content.content_id}" 
         initial_id="${component.content.content_id}" 
         style="text-align:left;"
         class="cms-dbstored">
      <h2 style="text-align: left;" 
          class="cms-editable-text" 
          onclick="cmp_paragraphpicture_edit(this, ${component.content.content_id}, true)"
          id="cmp_paragraphpicture_title_${component.content.content_id}">
        ${h.literal(data['title'])}
      </h2>
      <br>
      <span style="float: left; height: 0px; display:block;overflow:hidden;"></span>
      <span style="z-index: 10; float: left; position: relative; clear: left; margin-top: 0px;">
        <a>
          <img src="/cms/images/sample-image.jpg">
        </a>
        <div style="display: block; font-size: 90%; margin-top: -10px; margin-bottom: 10px; text-align: center;"></div>
      </span>
      <div style="text-align: left; display: block;"
           class="cms-editable-text" 
           id="cmp_paragraphpicture_body_${component.content.content_id}"
           onclick="cmp_paragraphpicture_edit(this, ${component.content.content_id}, true)">
        ${h.literal(data['body'])}
      </div><br>
    </div>
</%def>

<%def name="render_edit_js(component)">

/* KB: [2010-11-19]: This is the data structure that is stored in cms_content.data */
var cmp_paragraphpicture_data = {
    id: null,
    title: null,
    body: null,
    img: {}
};

cmp_paragraphpicture_edit = function(elem, id, is_existing) {
    page_edit_text(elem, id, 
                   function(elem, id) {
                       cmp_paragraphpicture_save(elem, id, is_existing);
                   });
};

cmp_paragraphpicture_save = function(elem, id, is_existing) {
    cmp_paragraphpicture_data = {id: id,
                                 title: null,
                                 body: null,
                                 img: {}};
    cmp_paragraphpicture_data.title = $("#cmp_paragraphpicture_title_"+id).html();
    cmp_paragraphpicture_data.body = $("#cmp_paragraphpicture_body_"+id).html();
    var arr = {};
    arr['data'] = pvs.json.encode(cmp_paragraphpicture_data);
    pvs.ajax.post_array(pvs.ajax.api({root: '/cms/content/save/paragraphpicture/'+$_('#site_id'), 
                                      content_id: (is_existing ? id : null)}),
                        function(response) {
                            var resp = pvs.json.decode(response);
                            if (resp.id) {
                                var orig_id = cmp_paragraphpicture_data.id;
                                cmp_paragraphpicture_data.id = resp.id;
                                 $('#cmp_paragraphpicture_div_'+id).wrap('<div id="div_'+resp.id+'"></div>');
                                $('#div_'+resp.id).empty();
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
       ${h.literal(html['html'])}
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
    ${h.textarea('cmp_paragraphpicture_html', style="width: 795px; height: 350px;", class_='html_editor')}
    </td>
  </tr>
</table>
</%def>


