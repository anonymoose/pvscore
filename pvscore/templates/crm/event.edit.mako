
<%inherit file="event.base.mako"/>\

<div> 
  <h1>Edit Event</h1>
  <div class="container">
    <form method="POST" id="frm_event" action="/crm/event/save">
      ${h.hidden('event_id', value=event.event_id)}
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="display_name">Display Name</label>
            ${h.text('display_name', size=50, value=event.display_name)}
          </div>
          <div class="span3">
            <label for="short_name">Short Name</label>
            ${h.text('short_name', size=50, value=event.short_name)}
          </div>
          <div class="span3">
            <label for="phase">Phase</label>
            ${h.text('phase', size=50, value=event.phase)}
          </div>
          <div class="span2">
            <label for="color">Color</label>
            ${h.text('color', size=50, value=event.color)}
          </div>
        </div>
        <div class="row">
          <div class="span3">
            <label for="event_type">Type</label>
            ${h.select('event_type', event.event_type, event_types)}
          </div>
          <div class="span3">
            ${h.checkbox('claim', checked=event.claim, label=' Claim')}
            ${h.checkbox('finalize', checked=event.finalize, label=' Finalize')}
            ${h.checkbox('is_system', checked=event.is_system, label=' Is System')}
          </div>
          <div class="span3">
            ${h.checkbox('milestone_complete', checked=event.milestone_complete, label=' Milestone Complete')}
            ${h.checkbox('note_req', checked=event.note_req, label=' Note Required')}
            ${h.checkbox('dashboard', checked=event.dashboard, label=' Dashboard')}
          </div>
          <div class="span2">
            <!--td nowrap>${h.checkbox('reason_req', checked=event.reason_req, label=' Reason Required')}</td-->
            ${h.checkbox('change_status', checked=event.change_status, label=' Change Status')}
            ${h.checkbox('touch', checked=event.touch, label=' Touch')}
          </div>
        </div>
        <div class="row">
          <div class="span2 offset10">
            <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>



