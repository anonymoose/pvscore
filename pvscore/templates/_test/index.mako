this is the index

campaign_id = ${request.ctx.campaign.campaign_id}


% for flash in request.session.pop_flash():
    ${flash}
% endfor


