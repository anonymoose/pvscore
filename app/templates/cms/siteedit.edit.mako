
<%inherit file="/cms/siteedit.base.mako"/>\

<%def name="left_col()">\
<div class="left_align_top">
  <h2>Sites</h2>
  <ul class="side-list">
    <li>${h.link_to('Edit Site Details', 'javascript:siteedit_show_site_edit()', id='link_add_page')}</li>
    <li>${h.link_to('Add Page', 'javascript:siteedit_add_page()', id='link_add_page')}</li>
    <li>${h.link_to('Pages', 'javascript:siteedit_show_pages()', id='link_show_pages')}</li>
    <li><hr/></li>
    <li>${h.link_to('List Sites', '/cms/siteedit/list')}</li>
    <li>${h.link_to('New Site', '/cms/siteedit/new')}</li>
  </ul>
</div>
</%def>

<div id="frm_site">
  <h1>Edit Site Details</h1>

  ${h.secure_form(h.url('/cms/siteedit/save'))}
  ${h.hidden('site_id', value=c.site.site_id)}

  <div class="_50">
    <label for="">Domain</label>
    ${h.text('domain', size=50, value=c.site.domain)}
  </div>
  <div class="_50">
    <label for="">Alias 1</label>
    ${h.text('domain_alias0', size=50, value=c.site.domain_alias0)}
  </div>
  <div class="clear"></div>
  <div class="_50">&nbsp;</div>
  <div class="_50">
    <label for="">Alias 2</label>
    ${h.text('domain_alias1', size=50, value=c.site.domain_alias1)}
  </div>
  <div class="clear"></div>
  <div class="_50">
    ${h.checkbox('maintenance_mode', checked=c.site.maintenance_mode, label='Maintenance Mode?')}
  </div>
  <div class="_50">
    <label for="">Alias 3</label>
    ${h.text('domain_alias2', size=50, value=c.site.domain_alias2)}
  </div>
  <div class="clear"></div>
  <div class="bump"></div>
  <div class="_50">
    <label for="">Company</label>
    ${h.select('company_id', c.site.company_id, c.companies)}
  </div>
  <div class="_50">
    <label for="">Default Campaign</label>
    ${h.select('default_campaign_id', c.site.default_campaign_id, c.campaigns)}
  </div>
  <div class="_50">
    <label for="">Title</label>
    ${h.text('seo_title', size=50, value=c.site.seo_title)}
  </div>
  <div class="_50">
    <label for="">Keywords</label>
    ${h.text('seo_keywords', size=50, value=c.site.seo_keywords)}
  </div>
  <div class="_50">
    <label for="">Description</label>
    ${h.text('seo_description', size=50, value=c.site.seo_description)}
  </div>
  <div class="clear"></div>
  <div class="_100">
    <label for="notes">Header Code</label>
    ${h.textarea('header_code', rows=5, style="width: 500px;", content=h.literal(c.site.header_code if c.site.header_code else ''))}
  </div>
  <div class="_100">
    <label for="notes">Footer Code</label>
    ${h.textarea('footer_code', rows=5, style="width: 500px;", content=h.literal(c.site.footer_code if c.site.footer_code else ''))}
  </div>
  <div class="_100">
    <label for="notes">robots.txt</label>
    ${h.textarea('robots_txt', rows=5, style="width: 500px;", content=h.literal(c.site.robots_txt if c.site.robots_txt else ''))}
  </div>
  <div class="_50">
    <label for="">Google Analytics Id</label>
    ${h.text('google_analytics_id', size=50, value=c.site.google_analytics_id)}
  </div>
  <div class="_50">
    <label for="">Shipping Method</label>
    ${h.select('shipping_method', c.site.shipping_method, c.shipping_methods)}
  </div>
  <div class="_50">
    <label for="">Tax Method</label>
    ${h.select('tax_method', c.site.tax_method, c.tax_methods)}
  </div>
  % if not c.site_config:
  <div class="_100"><font color="red"><b>site.config file is not present</b></font></div>
  % endif
  <div class="_100">Web Directory: ${c.site.site_web_directory('')}</div>
  <div class="align-right">
    ${h.submit('submit', 'Submit', class_="form-button")}
  </div>
  ${h.end_form()}
</div>

<div id="div_site_detail" style="display:none;">
</div>

<%def name="draw_body()">\
${self.draw_body_no_right_col()}
</%def>
