
<%inherit file="page.base.mako"/>\

<h1>${c.site.domain} -- Page List</h1>

<div id="result_list">
  <table width="100%" class="sortable">
    <thead>
      <tr>
        <th>Name</th>
        <th>Path</th>
        <th>Created</th>
        <th>Creator</th>
        <th align="left" nowrap>Top Level?</th>
        <th align="left">Published?</th>
      </tr>
    </thead>
    % for p in c.pages:
    <tr>
      <td class="pub_${p.published}"><a href="/cms/page/edit/${p.site.site_id}/${p.page_id}">${p.name}</a></td>
      <td class="pub_${p.published}">${p.url_path}</td>
      <td nowrap class="pub_${p.published}">${p.create_dt}</td>
      <td class="pub_${p.published}">${p.user_created}</td>
      <td class="pub_${p.published}">${'Y' if p.top_level_menu else ''}</td>
      <td class="pub_${p.published}">${'Y' if p.published else ''}</td>
    </tr>
    % endfor
  </table>
</div>

