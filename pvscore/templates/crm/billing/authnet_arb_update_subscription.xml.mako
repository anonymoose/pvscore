<?xml version="1.0" encoding="utf-8"?>
<ARBUpdateSubscriptionRequest xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd">
	<merchantAuthentication>
		<name>${auth_login}</name>
		<transactionKey>${auth_key}</transactionKey>
	</merchantAuthentication>
	<subscriptionId>${subscription_id}</subscriptionId>
	<subscription>
		<payment>
			<creditCard>
				<cardNumber>${card_number}</cardNumber>
				<expirationDate>${exp_date}</expirationDate>
			</creditCard>
		</payment>
	</subscription>
</ARBUpdateSubscriptionRequest>
