
<%inherit file="product.base.mako"/>\

<h1>Product Quick Editor</h1>

    <div id="inventory_container"><table id="inventory"></table></div>
    <div id="pager_container"><div id="pager"></div></div>

<script>

var column_names = ["", "ID", "Name", "SKU", "Manufacturer", "Inventory", "Inv Par", "$ Unit Cost"
% if len(campaigns):
  % for cmp in campaigns:
    ,"$ ${cmp.name}"
  % endfor
% endif
];

var column_model = [{name:"act",index:"act", width:18,sortable:false},
                    {name:"product_id",index:"product_id", width:2}, 
                    {name:"name",index:"name", width:180, editable:true}, 
                    {name:"sku",index:"sku", width:60, editable:true}, 
                    {name:"manufacturer",index:"manufacturer", width:120, editable: true},
                    {name:"inventory", index:"inventory", width:50, editable: true, editrules:{number:true}},
                    {name:"inventory_par", index:"inventory_par", width:50, editable: true, editrules:{number:true}},
                    {name:"unit_cost", index:"unit_cost", width:50, editable: true, editrules:{number:true}}
% if len(campaigns):
  % for cmp in campaigns:
        ,{name:"cmp_${cmp.campaign_id}", index:"cmp_${cmp.campaign_id}", width:50, editable: true, editrules:{number:true}}
  % endfor
% endif

                   ];

var products = {};
    % for i,p in enumerate(products):
        products['${p.product_id}'] = {name: '${p.name}',
                               manufacturer: '${p.manufacturer}',
                               inventory: '${p.inventory}'};
    % endfor
</script>



<%def name="draw_body()">\
${self.draw_body_center_only()}
</%def>

