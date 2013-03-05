
<%inherit file="site.base.mako"/>\

<div>
  % if not asset.id:
  <h2>Add File to ${site.domain}</h2>
  % else:
  <h2>Edit File to ${site.domain}</h2>
  % endif

  <div class="container">
    <form id="frm_asset" method="POST" enctype="multipart/form-data" action="/cms/content/file/save/${site.site_id}">
      ${h.hidden('asset_id', value=asset.id)}
      <div class="row">
        <div class="span9">
          <div class="well">
            <div class="row">
              <div class="span3">
                <label for="">Name</label>
                ${h.text('name', class_="input-xlarge", value=asset.name)}
              </div>
            </div>
            % if asset.id:
            <div class="row">
              <div class="span8">
                <label for="">Link to this image</label>
                <p>
                ${asset.absolute_path}
                </p>
              </div>
            </div>
            <div class="row">
              <div class="span8">
                <label for="">Uploaded Image</label>
                <img src="${asset.absolute_path}" style="max-height:400px;"/>
              </div>
            </div>
            % endif
            <div class="row">
              <div class="span3">
                <label for="">Select file to upload</label>
                <input type="file" name="Filedata"/>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="span2 offset7">
              <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
              <a href="/cms/content/file/list/${site.site_id}" class="btn btn-link">Cancel</a>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>


