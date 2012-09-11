<%def name="render(component)">
<%
if c.mode == 'edit_js':
    self.render_edit_js(component)
elif c.mode == 'create':
    self.render_create(component)
elif c.mode == 'edit':
    self.render_edit(component)
elif c.mode == 'call':
    func = getattr(self, c.function)
    func(component)
elif c.mode == 'view':
    self.render_view(component)
elif c.mode == 'view_js':
    pass
else:
    self.render_view_js(component)
    self.render_view(component)
%>
</%def>

<%def name="render_create(component)">
</%def>
<%def name="render_edit(component)">
</%def>
<%def name="render_edit_js(component)">
</%def>

<%def name="render_view(component)">
</%def>
<%def name="render_view_js(component)">
</%def>
<%def name="render_view_css(component)">
</%def>

${next.body()}


