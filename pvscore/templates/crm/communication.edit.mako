
<%inherit file="communication.base.mako"/>\

<div style="height:1500px">
  <h1>Edit Email Template</h1>
  <div class="container">
    <form method="POST" id="frm_comm" action="/crm/communication/save">
      ${h.hidden('comm_id', value=comm.comm_id)}
      <h3>General Information</h3>
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="name">Name</label>
            ${h.text('name', size=50, value=comm.name)}
          </div>
          <div class="span3">
            <label for="from_addr">From</label>
            ${h.text('from_addr', size=50, value=comm.from_addr)}
          </div>
          <div class="span3">
            <label for="subject">Subject</label>
            ${h.text('subject', size=50, value=comm.subject)}
          </div>
          <div class="span2">
            <label for="type">Type</label>
            ${h.select('type', comm.type, comm_types, onchange='comm_type_change()')}
          </div>
        </div>
        <div class="row">
          <div class="span3">
            ${h.checkbox('user_sendable', checked=comm.user_sendable, label=' Can be sent by users?')}
          </div>
          <div class="span5" id="row_url">
            <label for="title">URL</label>
            ${h.text('url', size=75, value=comm.url)}
          </div>
        </div>
      </div>
      <div class="row">
        <div class="span8" id="row_html">
          <label for="description"><h3>Email Template</h3></label>
          ${h.textarea('data', style="width: 800px; height: 520px;", content=h.literal(comm.data if comm.data else ''), class_='content_editor')}
        </div>
      </div>
      <div class="row">
        <div class="span3">
          <table>
            <tr><th>Click a token to insert it</th></tr>
            <tr valign="top">
              <td>
                <table>
                  % for t in comm_tokens[0:25]:
                  <tr><td><a href="javascript:comm_insert_token('${t}')">${t}</a></td></tr>
                  % endfor
                </table>
              </td>
              <td>
                <table>
                  % for t in comm_tokens[25:]:
                  <tr><td><a href="javascript:comm_insert_token('${t}')">${t}</a></td></tr>
                  % endfor
                </table>
              </td>
            </tr>
          </table>
        </div>
      </div>
      <div class="row">
        <div class="span2 offset10">
          <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
        </div>
      </div>
    </form>
  </div>
</div>

<%def name="other_foot()">\
<script>
  comm_init();
</script>
</%def>

<%def name="draw_body()">\
${self.draw_body_no_left_col()}
</%def>
