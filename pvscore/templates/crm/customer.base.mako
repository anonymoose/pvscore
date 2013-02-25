<%inherit file="base.mako"/>\

${next.body()}

<%def name="other_foot()">\
  <script type="text/javascript" src="https://js.stripe.com/v1/"></script>
  <script>
    Stripe.setPublishableKey('${request.ctx.enterprise.get_attr('stripe_public_key')}');
  </script>
</%def>

