item_count=cart.item_count
% for item in cart.items:
    product_id=${item['product'].product_id}
    has_product=${cart.has_product_id(item['product'].product_id)}
    product_name=${item['product'].name}
% endfor

total=cart.total
product_total=cart.product_total
handling=cart.handling_total
