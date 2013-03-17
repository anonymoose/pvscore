<RateV3Request USERID="{{ config.userid }}" PASSWORD="{{ config.password }}">
{% ifequal config.ship_type "FIRST CLASS" %}
    {% for type in first_class_types %}
    <Package ID="products{{ forloop.counter }}">
        <Service>{{ config.ship_type }}</Service>
        {% ifequal config.ship_type "FIRST CLASS" %}<FirstClassMailType>{{ type }}</FirstClassMailType>{% endifequal %}
        <ZipOrigination>{{ config.shop_details.postal_code}}</ZipOrigination>
        <ZipDestination>{{ contact.shipping_address.postal_code|slice:":5"}}</ZipDestination>
        <Pounds>{{ weight|pounds }}</Pounds>
        <Ounces>{{ weight|ounces }}</Ounces>
        <Container>{{ configcontainer }}</Container>
        <Size>REGULAR</Size>
        <Machinable>{% ifequal config.ship_type "FIRST CLASS" %}true{% else %}{% ifequal config.ship_type "PARCEL POST" %}true{% else %}{% ifequal config.ship_type "ALL" %}true{% else %}false{% endifequal %}{% endifequal %}{% endifequal %}</Machinable>
    </Package>
    {% endfor %}
{% else %}
    <Package ID="products">
        <Service>{{ config.ship_type }}</Service>
        {% ifequal config.ship_type "FIRST CLASS" %}<FirstClassMailType>{{ type }}</FirstClassMailType>{% endifequal %}
        <ZipOrigination>{{ config.shop_details.postal_code}}</ZipOrigination>
        <ZipDestination>{{ contact.shipping_address.postal_code|slice:":5"}}</ZipDestination>
        <Pounds>{{ weight|pounds }}</Pounds>
        <Ounces>{{ weight|ounces }}</Ounces>
        <Container>{{ configcontainer }}</Container>
        <Size>REGULAR</Size>
        <Machinable>{% ifequal config.ship_type "FIRST CLASS" %}true{% else %}{% ifequal config.ship_type "PARCEL POST" %}true{% else %}{% ifequal config.ship_type "ALL" %}true{% else %}false{% endifequal %}{% endifequal %}{% endifequal %}</Machinable>
    </Package>
{% endifequal %}
</RateV3Request

    
