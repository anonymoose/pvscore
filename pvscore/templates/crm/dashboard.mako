<%inherit file="base.mako"/>\


<div id="dashboard" class="container " >
  <h2>Dashboard</h2>
  <p>
    <div class="row">
      <div id="chart_0" class="span4"> </div>
      <div id="chart_1" class="span4"> </div>
      <div id="chart_2" class="span4"> </div>
    </div>
    <div class="row">
      <div id="chart_3" class="span4"> </div>
      <div id="chart_4" class="span4"> </div>
      <div id="chart_5" class="span4"> </div>
    </div>
  </p>
</div>


<%def name="other_foot()">\
<script>
$(document).ready(function() {
  % for i in range(len(charts)):
  $('#chart_'+'${i}').append('<img src="${charts[i].link(300,300,i)}" height="300" width="300"/>');
  % endfor
});
</script>
</%def>


<%def name="draw_body()">\
  ${self.draw_body_center_only()}
</%def>


