
<%inherit file="site.base.mako"/>\

<div>
  % if site.site_id:
  <h2>Edit Site Details</h2>
  % else:
  <h2>New Site Details</h2>
  % endif
  <div class="container">
    <form id="frm_site" method="POST" action="/cms/site/save">
      ${h.hidden('site_id', value=site.site_id)}
      <div class="row">
        <div class="span9">
       
          <div class="well">
            <div class="row">
              <div class="span3">
                <label for="">Domain</label>
                ${h.text('domain', value=site.domain)}
              </div>
            </div>
            <div class="row">
              <div class="span3">
                <label for="">Alias 1</label>
                ${h.text('domain_alias0', value=site.domain_alias0)}
              </div>
              
              <div class="span3">
                <label for="">Alias 2</label>
                ${h.text('domain_alias1', value=site.domain_alias1)}
              </div>
              
              <div class="span2">
                  <label for="">Alias 3</label>
                  ${h.text('domain_alias2', value=site.domain_alias2)}
              </div>
            </div>
            <div class="row">
              <div class="span3">
                <label for="">Company</label>
                ${h.select('company_id', str(site.company_id), companies)}
              </div>
              <div class="span3">
                <label for="">Default Campaign</label>
                ${h.select('default_campaign_id', str(site.default_campaign_id), campaigns)}
              </div>
            </div>
            <div class="row">
              <div class="span3">
                <label for="">&nbsp;</label>
                ${h.chkbox('maintenance_mode', checked=site.maintenance_mode, label='Maintenance Mode?')}
              </div>
              <div class="span2">
                <label for="">Namespace</label>
                ${h.text('namespace', value=site.namespace)}
              </div>
            </div>
            <div class="row">
              <div class="span3">
                <label for="">Title</label>
                ${h.text('seo_title', value=site.seo_title)}
              </div>
              <div class="span3">
                <label for="">Keywords</label>
                ${h.text('seo_keywords', value=site.seo_keywords)}
              </div>
              <div class="span2">
                  <label for="">Description</label>
                  ${h.text('seo_description', value=site.seo_description)}
              </div>
            </div>
            <div class="row">
              <div class="span5">
                <label for="notes">Site Config JSON</label>
                ${h.textarea('config_json', rows=5, style="width: 450px;", content=h.literal(site.config_json if site.config_json else ''))}
              </div>
            </div>
            <div class="row">
              <div class="span5">
                <label for="notes">robots.txt</label>
                ${h.textarea('robots_txt', rows=5, style="width: 450px;", content=h.literal(site.robots_txt if site.robots_txt else ''))}
              </div>
            </div>
            <div class="row">
              <div class="span3">
                  <label for="">Google Analytics Id</label>
                  ${h.text('google_analytics_id', value=site.google_analytics_id)}
              </div>
              <div class="span3">
                  <label for="">Shipping Method</label>
                  ${h.select('shipping_method', site.shipping_method, shipping_methods)}
              </div>
              <div class="span2">
                  <label for="">Tax Method</label>
                  ${h.select('tax_method', site.tax_method, tax_methods)}
              </div>
            </div>
          </div>
          <div class="row">
            <div class="span2 offset7">
              <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
              <a href="/cms/site/list" class="btn btn-link">Cancel</a>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>

<div id="div_site_detail" style="display:none;">
</div>

    
