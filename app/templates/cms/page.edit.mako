
<%inherit file="/cms/page.base.mako"/>\

<%def name="left_col()">\
<div class="left_align_top">
  <h2>Sites</h2>
  <ul class="side-list">
    <li>${h.link_to('Site Page List', '/cms/siteedit/edit/%s' % c.site.site_id, id='link_add_page')}</li>
    <li><hr/></li>
    <li>${h.link_to('List Sites', '/cms/siteedit/list')}</li>
    <li>${h.link_to('New Site', '/cms/siteedit/new')}</li>
    <li><hr/></li>
    <li>${h.link_to('List Templates', '/cms/template/list')}</li>
    <li>${h.link_to('New Template', '/cms/template/new')}</li>
  </ul>
</div>
</%def>

<div id="frm_page"> 
  <h1>Edit Page</h1>
  ${h.secure_form(h.url('/cms/page/save'))}
  ${h.hidden('site_id', value=c.site.site_id)}
  ${h.hidden('page_id', value=c.page.page_id)}
  <div class="_50">
    <label for="">Name</label>
    ${h.text('name', size=50, value=c.page.name)}
  </div>
  <div class="clear"></div>
  <div class="_100">
    <label for="">Title</label>
    ${h.text('seo_title', size=50, value=c.page.seo_title)}
  </div>
  <div class="_100">
    <label for="">Keywords</label>
    ${h.text('seo_keywords', size=50, value=c.page.seo_keywords)}
  </div>
  <div class="_100">
    <label for="">Description</label>
    ${h.text('seo_description', size=50, value=c.page.seo_description)}
  </div>
  <div class="_50">
    <label for="">URL Path</label>
    ${h.text('url_path', size=50, value=c.page.url_path)}
  </div>
  <div class="_50">
    <label for="">Site Root?</label>
    ${h.checkbox('site_root', checked=c.page.site_root)}
  </div>
  <div class="_50">
    <label for="">Published?</label>
    ${h.checkbox('published', checked=c.page.published)}
  </div>
  <div class="_50">
    <label for="">Top Level Menu?</label>
    ${h.checkbox('top_level_menu', checked=c.page.top_level_menu)}
  </div>
  <div class="_50">
    <label for="">Menu Sort Order</label>
    ${h.text('menu_sort_order', size=2, value=c.page.menu_sort_order)}
  </div>
  <div class="_50">
    <label for="">Track Hits?</label>
    ${h.checkbox('track', checked=c.page.track)}
  </div>
  <div class="_50">
    <label for="">Password Protected?</label>
    ${h.checkbox('protected', checked=c.page.protected)}
  </div>
  <div class="clear"></div>
  <div class="_50">
    <label for="">Access Denied URL</label>
    ${h.text('access_denied_url', size=50, value=c.page.access_denied_url)}
  </div>
  <div class="_50">
    <label for="">Redirect URL</label>
    ${h.text('redirect_url', size=50, value=c.page.redirect_url)}
  </div>
  <div class="_50">
    <label for="">Template</label>
    ${h.select('template_id', c.page.template_id, c.templates)}
  </div>
  <div class="clear"></div>
  <div class="align-right">
    ${h.submit('submit', 'Submit', class_="form-button")}
  </div>
  ${h.end_form()}
</div>
<hr>
<div id="content">
  <h3>Edit Content Blocks</h3>
  ${h.secure_form(h.url('/cms/content/save'))}
  ${h.hidden('site_id', value=c.site.site_id)}
  ${h.hidden('page_id', value=c.page.page_id)}
  <table>
    % for cont in c.placeholders:
    <tr valign="top">
      <td>${cont.name}</td>
      <td>
        % if 'html' == cont.type:
        ${h.textarea('data_%s' % cont.name, style="width: 100%; height: 100px;", content=h.literal(cont.data if cont.data else ''), class_='content_editor')}</td>
        % elif 'string' == cont.type:
        ${h.text('data_%s' % cont.name, size=60, value=h.literal(cont.data if cont.data else ''))}</td></tr>
        % endif
      </td>
    </tr>
    % endfor
    <tr><td colspan="3" align="right">${h.submit('submit', 'Save Content', class_="form-button")}<td></tr>          
  </table>
  ${h.end_form()}
</div>

<script>
  page_setup_textarea();
</script>

<%def name="draw_body()">\
${self.draw_body_no_right_col()}
</%def>
