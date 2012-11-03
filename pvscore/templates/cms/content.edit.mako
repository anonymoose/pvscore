
<%inherit file="site.base.mako"/>\

<div>
  % if content.content_id:
  <h2>Edit Content Block</h2>
  % else:
  <h2>New Content Block</h2>
  % endif
  <div class="container">
    <form id="frm_site" method="POST" action="/cms/content/save">
      ${h.hidden('site_id', value=site.site_id)}
      ${h.hidden('content_id', value=content.content_id)}
      <div class="row">
        <div class="span9">
          <div class="well">
            <div class="row">
              <div class="span3">
                <label for="">Name</label>
                ${h.text('name', class_="input-xlarge", value=content.name)}
              </div>
            </div>
            <div class="row">
              <div class="span8">
                <label for="notes">Content</label>
                ${h.textarea('data', style="width: 800px; height: 520px;", content=h.literal(content.data if content.data else ''), class_='content_editor')}
              </div>
            </div>
          </div>
          <div class="row">
            <div class="span2 offset7">
              <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
              <a href="/cms/content/list/${site.site_id}" class="btn btn-link">Cancel</a>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>


<%def name="other_foot()">\
<script>
  content_init();
</script>
</%def>


    
