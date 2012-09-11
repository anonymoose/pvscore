## inherit from super_component so you get frameworky functionality.
<%inherit file="../super_component.mako"/>\

<%!
# This is module level functionality that is declared and executed once on
# pylons startup.
from app.lib.component import BaseComponent
from app.model.cms.page import Page
import re, pdb

class PictureComponent(BaseComponent):
    def __init__(self, component_type, content=None):
        self.component_type = component_type
        self.content = content
        self.initial_id = BaseComponent.generate_initial_id()
%>

<%
# This gets run everytime.  You have to call it just like this so that your
# superclass methods get called in the right order by mode.
component = PictureComponent(c.content_type, c.content if hasattr(c, 'content') else None)
self.render(component)
%>

##
## define methods here that get called by the superclass.  If you want to call
## one of these methods from the browser, call it via
## /cms/content/component/call/{short_name}/{method}
## example: 
## /cms/content/component/call/picture/show_edit_dialog
##

## render_create()
## called when the component is dragged into an editable region.
## "initial_id" is used to give the framework something to reference back to on creation
## later in render_edit() it is used to hold content_id of the saved content
<%def name="render_create(component)">
    <img id="cmp_picture_img_${component.initial_id}" 
         initial_id="${component.initial_id}" 
         src="/cms/images/sample-image.jpg" 
         onclick="cmp_picture_edit_image(this)"/>
</%def>

## render_edit()
## called when the component is dragged into an editable region.
## initial_id is used to hold content_id.  You add the "class=cms-dbstored" attribute
## to indicate that this guy came from the database and we can search for it later.
<%def name="render_edit(component)">
<%
    data = component.content.data
    pic = component.content.data_to_json()
    height = 'height="%s"' % pic['height'] if pic['height'] else ''
    width = 'width="%s"' % pic['width'] if pic['width'] else ''
%>
    <img id="cmp_picture_img_${component.content.content_id}" 
         initial_id="${component.content.content_id}" 
         ${h.literal(height)} ${h.literal(width)}
         src="${pic['path']}" 
         style="${pic['border']} ${pic['margin_top']} ${pic['margin_bottom']} ${pic['margin_left']} ${pic['margin_right']}"
         alt="${pic['caption']}"
         class="cms-dbstored"
         onclick="cmp_picture_edit_image(this, ${component.content.content_id})"/>
</%def>

## render_edit_js()
## called when the component is dragged into an editable region.  Only put in JS
## here.  Do not wrap in script tag.  This will get called exactly once per session and each of the components code 
## blocks are available.
<%def name="render_edit_js(component)">

/* KB: [2010-11-19]: This is the data structure that is stored in cms_content.data */
var cmp_picture_data = {
        id: null,
        path: null,
        width: 0,
        height: 0,
        caption: null,
        border: null,
        position: null,
        onclick: null,
        margin_top: 0,
        margin_bottom: 0,
        margin_left: 0,
        margin_right: 0
};

/* KB: [2010-11-19]: If the component is new (just dragged) then this will be null.  otherwise
it will contain cms_content.content_id of the thing we are working with. */
var cmp_picture_existing_id = null;

/* KB: [2010-11-19]: Called when the element is clicked.  Be ready to edit existing and edit new.
   Since there is no DB ID initially, we get one from the system via Picture.initial_id.  This ID will
   be replaced with the one from the database after it is persisted.
 */
cmp_picture_edit_image = function(placeholder, existing_id) {
    cmp_picture_existing_id = null;
    var initial_id = $(placeholder).attr('initial_id');
    cmp_picture_clear_tmp_data();
    pvs.dialog.display({url:pvs.ajax.api({root: '/cms/content/component/call/picture/show_edit_dialog'}),
                        title: 'Add Image',
                        width:830, 
                        height:520,
                        after_display_impl:
                        function() {
                            var url = pvs.ajax.api({root: '/cms/asset/upload', 
                                                       site_id: $_('#site_id'), 
                                                       page_id: $_('#page_id')});
                            $('#file_upload').uploadify({
                                'uploader'     : '/public/js/jquery-1.4.2/jquery.uploadify-v2.1.4/uploadify.swf',
                                'script'       : url,
                                'cancelImg'    : '/public/js/jquery-1.4.2/jquery.uploadify-v2.1.4/cancel.png',
                                'folder'       : '/images',
                                'fileExt'      : '*.jpg;*.gif;*.png',
                                'scriptAccess' : 'sameDomain',
                                'wmode'        : 'transparent',
                                'auto'         : true,
                                'onComplete'   : function(event, ID, fileObj, response, data) {
                                    cmp_picture_data.path = response;
                                    var id = cmp_picture_data.id = initial_id;
                                    $('#uploaded_image').html('<img id="cmp_picture_popup_'+cmp_picture_data.id+'" src="'+cmp_picture_data.path+'" border="0"/>');
                                },
                                'onError'      : function (event,ID,fileObj,errorObj) {
                                    alert(errorObj.type + ' Error: ' + errorObj.info);
                                }
                            });
                            if (existing_id) {
                                pvs.ajax.call(pvs.ajax.api({root: '/cms/content/show_data/'+existing_id}),
                                                             function(response) {
                                                                 cmp_picture_existing_id = existing_id;
                                                                 cmp_picture_data = pvs.json.decode(response);
                                                                 cmp_picture_data.id = existing_id;
                                                                 $('#uploaded_image').html('<img id="cmp_picture_popup_'+existing_id+'"/>');
                                                                 cmp_picture_edit_update_image('cmp_picture_popup');
                                                                 cmp_picture_edit_update_vars();
                                                             });
                            }
                        },
                        on_before_close:
                        function() {
                            cmp_picture_update_tmp_data();
                            return true;
                        },
                        on_ok: 
                        function() {
                            cmp_picture_save();
                        }
                });
};

/* KB: [2010-11-19]: When we click OK or blur one of the attributes we want the representation in the popup to 
   change on the fly.  This ensures that it happens.
 */
cmp_picture_edit_update = function(selector) {
    cmp_picture_clear_tmp_data(true);
    cmp_picture_update_tmp_data();
    cmp_picture_edit_update_image(selector);
};

cmp_picture_clear_tmp_data = function(preserve_readonly) {
    if (!preserve_readonly) {
        cmp_picture_data.id = null;
        cmp_picture_data.path = null;
    }
    cmp_picture_data.width = null;
    cmp_picture_data.height = null;
    cmp_picture_data.caption = null;
    cmp_picture_data.border = null;
    cmp_picture_data.position = null;
    cmp_picture_data.onclick = null;
    cmp_picture_data.margin_top = null;
    cmp_picture_data.margin_bottom = null;
    cmp_picture_data.margin_left = null;
    cmp_picture_data.margin_right = null;
};

cmp_picture_update_tmp_data = function() {
    cmp_picture_data.width = $_('#cmp_picture_width');
    cmp_picture_data.height = $_('#cmp_picture_height');
    cmp_picture_data.caption = $_('#cmp_picture_caption');
    cmp_picture_data.border = $_('#cmp_picture_border');
    cmp_picture_data.position = $_('#cmp_picture_position');
    cmp_picture_data.onclick = $_('#cmp_picture_onclick');
    cmp_picture_data.margin_top = $_('#cmp_picture_margin_top');
    cmp_picture_data.margin_bottom = $_('#cmp_picture_margin_bottom');
    cmp_picture_data.margin_left = $_('#cmp_picture_margin_left');
    cmp_picture_data.margin_right = $_('#cmp_picture_margin_right');
};

/* KB: [2010-11-19]: When we load up from a persisted one we need to set the vars to the values from the database. */
cmp_picture_edit_update_vars = function() {
    $('#cmp_picture_width').val(cmp_picture_data.width);
    $('#cmp_picture_height').val(cmp_picture_data.height);
    $('#cmp_picture_caption').val(cmp_picture_data.caption);
    $('#cmp_picture_border').val(cmp_picture_data.border);
    $('#cmp_picture_position').val(cmp_picture_data.position);
    $('#cmp_picture_onclick').val(cmp_picture_data.onclick);
    $('#cmp_picture_margin_top').val(cmp_picture_data.margin_top);
    $('#cmp_picture_margin_bottom').val(cmp_picture_data.margin_bottom);
    $('#cmp_picture_margin_left').val(cmp_picture_data.margin_left);
    $('#cmp_picture_margin_right').val(cmp_picture_data.margin_right);
};

/* KB: [2010-11-19]: Create the HTML that actually gets shown.  
   selector can be set to the one in the popup (cmp_picture_popup_+cmp_picture_data.id)
   or the one on the page (cmp_picture_img_${component.initial_id}).  The code executes the same for both
   and through the magic of jquery, it instantly changes the look on the page for visual feedback.
 */
cmp_picture_edit_update_image = function(selector) {
    var img_id = '#'+selector+'_'+cmp_picture_data.id;
    $(img_id).attr('src', cmp_picture_data.path);
    if (cmp_picture_data.width) {
        $(img_id).attr('width', cmp_picture_data.width);
    } else {
        $(img_id).removeAttr('width');
    }
    if (cmp_picture_data.height) {
        $(img_id).attr('height', cmp_picture_data.height);
    } else {
        $(img_id).removeAttr('height');
    }
    if (cmp_picture_data.position) {
        $(img_id).parent().css('text-align', cmp_picture_data.position)
    }
    if (cmp_picture_data.onclick) {
        $(img_id).attr('onclick', cmp_picture_data.onclick);
    }

    $(img_id).attr('style', cmp_picture_data.border +
                            cmp_picture_data.margin_top +
                            cmp_picture_data.margin_bottom +
                            cmp_picture_data.margin_left +
                            cmp_picture_data.margin_right);
    if (cmp_picture_data.caption) {
        $(img_id).attr('alt', cmp_picture_data.caption);
    } else {
        $(img_id).removeAttr('alt');
    }
};

/* KB: [2010-11-19]: Save the thing to the database.  Its only necessary to send the cmp_picture_data structure
   as a string of json.  If content_id is empty, then it inserts.  If its not empty then it updates.
   After we save in the dialog, we re-render the actual element on the page from the DB to ensure everything is ok.

   After we are done, we need to tell the page level management that we are done and it can save the layout 
   (which is just the ordering of the component IDs).  Notifying the page that things should be saved should be
   done after the re-rendering.
 */
cmp_picture_save = function() {
    var arr = {};
    arr['data'] = pvs.json.encode(cmp_picture_data);
    pvs.ajax.post_array(pvs.ajax.api({root: '/cms/content/save/picture/'+$_('#site_id'), 
                                      content_id: cmp_picture_existing_id}),
                        function(response) {
                            var resp = pvs.json.decode(response);
                            if (resp.id) {
                                var orig_id = cmp_picture_data.id;
                                cmp_picture_data.id = resp.id;
                                if (orig_id != resp.id) {
                                    // this is the first save.
                                    $('#cmp_picture_img_'+orig_id).attr('id', 'cmp_picture_img_'+resp.id);
                                }
                                cmp_picture_edit_update_image('cmp_picture_img');
                                $('#cmp_picture_img_'+cmp_picture_data.id).wrap('<div id="div_'+resp.id+'"></div>');
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
    pic = component.content.data_to_json()
    height = 'height="%s"' % pic['height'] if pic['height'] else ''
    width = 'width="%s"' % pic['width'] if pic['width'] else ''
    position = 'style="text-align:%s;"' % pic['position'] if pic['position'] else ''
%>
    <div ${h.literal(position)}>
    <img id="cmp_picture_img_${component.content.content_id}" 
         ${h.literal(height)} ${h.literal(width)}
         src="${pic['path']}" 
         style="${pic['border']} ${pic['margin_top']} ${pic['margin_bottom']} ${pic['margin_left']} ${pic['margin_right']}"
         onclick="${pic['onclick']}"
         alt="${pic['caption']}"/>
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
        Please choose an image from your computer.
      </p>
      <p>
        Images must be JPG, GIF, or PNG and less than 10 MB.
      </p>
    </td>
  </tr>
  <tr>
    <td width="70%" valign="top" style="overflow: scroll;"> <!-- left column -->
      <table>
        <tr>
          <td>
            <input id="file_upload" name="file_upload" type="file" />
          </td>
        </tr>
        <tr>
          <td><div id="uploaded_image"></div></td>
        </tr>
      </table>
    </td>
    <td valign="top"> <!-- right column -->
      <table>
        <tr><td nowrap>Width</td><td>${h.text('cmp_picture_width', size=5, onblur="cmp_picture_edit_update('cmp_picture_popup')")}</td></tr>
        <tr><td nowrap>Height</td><td>${h.text('cmp_picture_height', size=5, onblur="cmp_picture_edit_update('cmp_picture_popup')")}</td></tr>
        <tr><td nowrap>Caption</td><td>${h.text('cmp_picture_caption', size=25, onblur="cmp_picture_edit_update('cmp_picture_popup')")}</td></tr>
        <tr><td nowrap>Border</td><td>${h.select('cmp_picture_border', None, [['border-width:0px;', 'None'], ['border-width:1px;', 'Small'], ['border-width:1px;padding:3px;', 'Medium'], ['border-width:1px;padding:6px;', 'Large']], onchange="cmp_picture_edit_update('cmp_picture_popup')")}</td></tr>
        <tr><td nowrap>Position</td><td>${h.select('cmp_picture_position', None, [['left', 'Left'], ['center', 'Center'], ['right', 'Right']], onchange="cmp_picture_edit_update('cmp_picture_popup')")}</td></tr>
        <tr><td nowrap>On Click</td><td>${h.text('cmp_picture_onclick', size=25, onblur="cmp_picture_edit_update('cmp_picture_popup')")}<td></tr>
        <tr><td nowrap>Top Margin</td><td>${h.select('cmp_picture_margin_top', None, [['margin-top:0px;', 'None'], ['margin-top:5px;', 'Small'], ['margin-top:10px;', 'Medium'], ['margin-top:15px;', 'Large']], onchange="cmp_picture_edit_update('cmp_picture_popup')")}</td></tr>
        <tr><td nowrap>Bottom Margin</td><td>${h.select('cmp_picture_margin_bottom', None, [['margin-bottom:0px;', 'None'], ['margin-bottom:5px;', 'Small'], ['margin-bottom:10px;', 'Medium'], ['margin-bottom:15px;', 'Large']], onchange="cmp_picture_edit_update('cmp_picture_popup')")}</td></tr>
        <tr><td nowrap>Left Margin</td><td>${h.select('cmp_picture_margin_left', None, [['margin-left:0px;', 'None'], ['margin-left:5px;', 'Small'], ['margin-left:10px;', 'Medium'], ['margin-left:15px;', 'Large']], onchange="cmp_picture_edit_update('cmp_picture_popup')")}</td></tr>
        <tr><td nowrap>Right Margin</td><td>${h.select('cmp_picture_margin_right', None, [['margin-right:0px;', 'None'], ['margin-right:5px;', 'Small'], ['margin-right:10px;', 'Medium'], ['margin-right:15px;', 'Large']], onchange="cmp_picture_edit_update('cmp_picture_popup')")}</td></tr>
      </table>
    </td>
  </tr>
</table>
</%def>


