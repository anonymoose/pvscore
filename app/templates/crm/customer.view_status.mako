
<%inherit file="customer.base.mako"/>\

<style>
.dl-x dd {
  text-align: left;
}
</style>


<dl class="dl-horizontal dl-x" style="text-overflow:clip;">
  <dt>Event</dt>
  <dd>${status.event.display_name}</dd>
  <dt>Type</dt>
  <dd>${status.fk_type}</dd>
  <dt>ID</dt>
  <dd>${status.fk_id}</dd>
  <dt>Create Dt</dt>
  <dd>${status.create_dt}</dd>
  <dt>Created By</dt>
  <dd>${status.username}</dd>
  <dt>Note</dt>
  <dd>${h.literal(status.note)}</dd>
</dt>







