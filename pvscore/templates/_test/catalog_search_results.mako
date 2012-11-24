

<pre>
% for i, product in enumerate(products):
------------------------------------------------
product_id=${product.product_id}
product_name=${product.name}
price=${h.money(product.get_price(campaign))}
discount=${h.money(product.get_discount_price(campaign))}
% endfor
</pre>
