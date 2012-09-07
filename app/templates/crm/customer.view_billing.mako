
<%inherit file="customer.base.mako"/>\

<style>
.dl-x dd {
  text-align: left;
}
</style>

<dl class="dl-horizontal dl-x" style="text-overflow:clip;">
  <dt>Type</dt>
  <dd>${journal.type}</dd>
  <dt>Create Dt</dt>
  <dd>${journal.create_dt}</dd>
  <dt>User</dt>
  <dd>${journal.user_created}</dd>
  <dt>Amount</dt>
  <dd>${journal.amount}</dd>
  <dt>Order</dt>
  <dd>${journal.order_id}</dd>
  <dt>Note</dt>
  <dd>${h.literal(journal.note)}</dd>
</dt>







