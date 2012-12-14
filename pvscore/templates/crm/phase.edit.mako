
<%inherit file="phase.base.mako"/>\

<div>
  <h1>Edit Phase</h1>
  <div class="container">
    <form method="POST" id="frm_phase" action="/crm/phase/save">
      ${h.hidden('phase_id', value=phase.phase_id)}
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="display_name">Display Name</label>
            ${h.text('display_name', size=50, value=phase.display_name)}
          </div>
          <div class="span3">
            <label for="short_name">Short Name</label>
            ${h.text('short_name', size=50, value=phase.short_name)}
          </div>
          <div class="span2">
            <label for="color">Color</label>
            ${h.text('color', size=50, value=phase.color)}
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



