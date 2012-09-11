${h.javascript_link('/public/js/jquery-1.4.2/core/jquery-1.4.2.js')}
${h.javascript_link('/public/js/jquery-current/barcode.2.0.2/jquery-barcode-2.0.2.min.js')}
${h.javascript_link('/public/js/pvs/pvs-jquery.js')}
${h.javascript_link('/public/crm/js/product.js')}

<html>
<body>
<input type="hidden" id="product_id" value="${c.product_id}">

<!-- <div id="barcode" style="height:75px;width:50px;"></div> -->
<canvas id="barcode" width="150" height="150"></canvas> 

<script>
product_gen_barcode(${c.product_id});
</script>

</body>
