% for opt in cart.shipping_options:
    ${opt['name']}
    ${h.money(opt['charges'])}
    <br>
% endfor
