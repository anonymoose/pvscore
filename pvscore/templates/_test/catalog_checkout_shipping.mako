% for opt in cart.shipping_options:
    ${opt['name']}
    ${h.money(opt['charges'])}
${opt['name']}/${opt['code']}
    <br>
% endfor
