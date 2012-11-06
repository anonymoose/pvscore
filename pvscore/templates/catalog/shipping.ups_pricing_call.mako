<?xml version="1.0"?>
<AccessRequest xml:lang="en-US">
  <AccessLicenseNumber>${api_key}</AccessLicenseNumber>
  <UserId>${user_id}</UserId>
  <Password>${password}</Password>
</AccessRequest>
<?xml version="1.0"?>
<RatingServiceSelectionRequest xml:lang="en-US">
  <Request>
    <TransactionReference>
      <CustomerContext>Rating and Service</CustomerContext>
      <XpciVersion>1.0</XpciVersion>
    </TransactionReference>
    <RequestAction>Rate</RequestAction>
    <RequestOption>Shop</RequestOption>
  </Request>
  <PickupType>
    <Code>${pickup}</Code>
    <Description>Rate</Description>
  </PickupType>
  <Shipment>
    <Description>Rate Description</Description>
    <Shipper>
      <Name>${company.name}</Name>
      <PhoneNumber>${company.phone.replace('-', '')}</PhoneNumber>
      <ShipperNumber>${account}</ShipperNumber>
      <Address>
        <AddressLine1>${company.addr1}</AddressLine1>
        % if company.addr2:
        <AddressLine2>${company.addr2}</AddressLine2> 
        % endif
        <City>${company.city}</City>
        <StateProvinceCode>${company.state}</StateProvinceCode>
        <PostalCode>${company.zip}</PostalCode>
        <CountryCode>${company.country if company.country else 'US'}</CountryCode>
      </Address>
    </Shipper>
    <ShipTo>
      <CompanyName>${cust.fname} ${cust.lname}</CompanyName>
      <PhoneNumber>${cust.phone.replace('-', '')}</PhoneNumber>
      <Address>
        <AddressLine1>${cust.addr1}</AddressLine1>
        % if cust.addr2: 
        <AddressLine2>${cust.addr2}</AddressLine2> 
        % endif
        <City>${cust.city}</City>
        <StateProvinceCode>${cust.state}</StateProvinceCode>
        <PostalCode>${cust.zip}</PostalCode> 
        <CountryCode>${cust.country if cust.country else 'US'}</CountryCode>
      </Address>
    </ShipTo>
    <ShipFrom>
      <CompanyName>${company.name}</CompanyName>
      <PhoneNumber>${company.phone.replace('-', '')}</PhoneNumber>
      <ShipperNumber>${account}</ShipperNumber>
      <Address>
        <AddressLine1>${company.addr1}</AddressLine1>
        % if company.addr2: 
        <AddressLine2>${company.addr2}</AddressLine2> 
        % endif
        <City>${company.city}</City>
        <StateProvinceCode>${company.state}</StateProvinceCode>
        <PostalCode>${company.zip}</PostalCode>
        <CountryCode>${company.country if company.country else 'US'}</CountryCode>
      </Address>
    </ShipFrom>
    <PaymentInformation>
      <Prepaid>
        <BillShipper>
          <AccountNumber>${account}</AccountNumber>
        </BillShipper>
      </Prepaid>
    </PaymentInformation>

    <Package>
      <PackagingType>
	<Code>${container}</Code>
        <Description>Customer Supplied</Description>
      </PackagingType>
      <Description>Package</Description>
      <PackageWeight>
        <UnitOfMeasurement>
          <Code>LBS</Code>
        </UnitOfMeasurement>
        <Weight>${total_weight}</Weight>
      </PackageWeight> 
    </Package>
  </Shipment>
</RatingServiceSelectionRequest>

