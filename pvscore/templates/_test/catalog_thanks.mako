<%
from pvscore.model.crm.customerorder import CustomerOrder
order_id = request.GET.get('order_id')
order = CustomerOrder.load(order_id)
%>

Thanks for your purchase

% for oitem in order.active_items:
  ${oitem.product.name}
  unit_price = ${oitem.unit_price}
  unit_discount_price = ${oitem.unit_discount_price}
  unit_retail_price = ${oitem.unit_retail_price}
  total = ${oitem.total()}
% endfor


order total_payments_applied = ${order.total_payments_applied()}
order total_discounts_applied = ${order.total_discounts_applied()}
order total_payments_due = ${order.total_payments_due()}
order total_price = ${order.total_price()}
order total_item_price = ${order.total_item_price()}
order total_shipping_price = ${order.total_shipping_price()}

