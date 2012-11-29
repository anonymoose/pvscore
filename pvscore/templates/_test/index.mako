this is the index

campaign_id = ${request.ctx.campaign.campaign_id}

% if request.ctx.customer:
customer_id = ${request.ctx.customer.customer_id}
% endif

% for flash in request.session.pop_flash():
    ${flash}
% endfor


