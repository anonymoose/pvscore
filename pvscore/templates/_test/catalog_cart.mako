item_count=cart.item_count
% for item in cart.items:
    product_id=${item['product'].product_id}
    quantity=${item['product'].product_id}/${item['quantity']}
    has_product=${cart.has_product_id(item['product'].product_id)}
    product_name=${item['product'].name}
% endfor

total=${cart.total}
product_base_total=${cart.product_base_total}
product_total=${cart.product_total}
product_discounts=${cart.product_discount_total}
handling=${cart.handling_total}


