<%inherit file="/crm2/base.mako"/>\

      ${next.body()}

<%def name="local_head()">\
  ${h.javascript_link_ex('/public/js/pvs/pvs-jquery.js')}
  ${h.javascript_link('/public/js/ckeditor_3.1/ckeditor.js')}
  ${h.javascript_link('/public/js/tinymce_3_2_0_1/tinymce/jscripts/tiny_mce/tiny_mce.js')}
  ${h.javascript_link('/public/js/jquery-1.4.2/jquery.uploadify-v2.1.4/swfobject.js')}
  ${h.javascript_link('/public/js/jquery-1.4.2/jquery.uploadify-v2.1.4/jquery.uploadify.v2.1.4.min.js')}
  ${h.javascript_link('/public/js/jquery-1.4.2/jquery.json-2.2/jquery.json-2.2.min.js')}
  ${h.javascript_link('/public/cms/js/siteedit.js')}
  ${h.javascript_link('/public/cms/js/page.js')}
</%def>

