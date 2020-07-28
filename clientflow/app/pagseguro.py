import xml.etree.ElementTree as ET
import requests

# token = 
# email =

def criarPlano(name,reference,valor):
    url = "https://ws.sandbox.pagseguro.uol.com.br/pre-approvals/request/?email="+email+"&token="+token
    payload = "<?xml version=\"1.0\" encoding=\"ISO-8859-1\" standalone=\"yes\"?>\r\n<preApprovalRequest>\r\n<preApproval>\r\n<name>"+name+"</name>\r\n<reference>"+reference+"</reference>\r\n<charge>AUTO</charge>\r\n<period>MONTHLY</period>\r\n<amountPerPayment>"+valor+"</amountPerPayment>\r\n<cancelURL>http://sitedocliente.com</cancelURL>\r\n<membershipFee>0.00</membershipFee>\r\n<trialPeriodDuration>1</trialPeriodDuration>\r\n</preApproval>\r\n<maxUses>1</maxUses>\r\n</preApprovalRequest>"
    headers = {
      'Accept': 'application/vnd.pagseguro.com.br.v3+xml;charset=ISO-8859-1',
      'Content-Type': 'application/xml;charset=ISO-8859-1'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    xmlResponse = ET.fromstring(response.text)[0]
    preApprovalRequest = xmlResponse.text
    if xmlResponse.tag == "error":
        return {"erro" : xmlResponse[0][1].text}
    return {"pg": preApprovalRequest}

def criarSession():
    url = "https://ws.sandbox.pagseguro.uol.com.br/v2/sessions?email="+email+"&token="+token
    payload = {}
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    session = ET.fromstring(response.text)[0].text
    return session

def criarHash(cn,cb,cvv,cem,cey):
    url = "https://df.uol.com.br/v2/cards"
    payload = 'sessionId=4eb97a0c24a24b518a883cbcce83ff9a&cardNumber='+cn+'&cardBrand='+cb+'&cardCvv='+cvv+'&cardExpirationMonth='+cem+'&cardExpirationYear='+cey
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    hash = ET.fromstring(response.text)[0].text
    return hash

def aderirPlano(plano,referencia,user):
    url = "https://ws.sandbox.pagseguro.uol.com.br/pre-approvals?email="+email+"&token="+token
    payload = {
    	"plan": plano,
    	"reference": referencia,
    	"sender": {
    		"name":  "usuario1",
    		"email": "nandbox@pagseguro.com.br",
    		"hash": "88775b5906cfba47886c0883a9b761097cb3d1f8455837c1eea4b9f7f1544b28",
    		"phone": {
    			"areaCode": "11",
    			"number": "20516250"
    		},
    		"address": {
    			"street": "Rua Vi Jose De Castro",
    			"number": "99",
    			"complement": "",
    			"district": "It",
    			"city": "Sao Paulo",
    			"state": "SP",
    			"country": "BRA",
    			"postalCode": "06240300"
    		},
    		"documents": [{
    			"type": "CPF",
    			"value": "68951723003"
    		}]
    	},
    	"paymentMethod": {
    		"type": "CREDITCARD",
    		"creditCard": {
    			"token": "dba59d6fb57d4f28906cc918bb9ee1e6",
    			"holder": {
    				"name": "Julian Teste",
    				"birthDate": "04/12/1991",
    				"documents": [{
    					"type": "CPF",
    					"value": "19333575090"
    				}],
    				"phone": {
    					"areaCode": "11",
    					"number": "20516250"
    				},
    				"billingAddress": {
    					"street": "Rua Vi Jose De Castro",
    					"number": "99",
    					"complement": "",
    					"district": "It",
    					"city": "Sao Paulo",
    					"state": "SP",
    					"country": "BRA",
    					"postalCode": "06240300"
    				}
    			}
    		}
    	}
    }
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.pagseguro.com.br.v1+json;charset=ISO-8859-1'
    }
    response = requests.request("POST", url, headers=headers, data = payload)

def cobrarPlano():
    url = "https://ws.sandbox.pagseguro.uol.com.br/pre-approvals/payment?email={{ADICIONE_SEU_EMAIL}}&token={{ADICIONE_SEU_TOKEN}}"
    payload = "<payment>\r\n\t<items>\r\n\t\t<item>\r\n\t\t\t<id>0001</id>\r\n\t\t\t<description>AUUUU</description>\r\n\t\t\t<amount>100.00</amount>\r\n\t\t\t<quantity>2</quantity>\r\n\t\t</item>\r\n\t</items>\r\n\t<reference>REF1234-1</reference>\r\n\t<preApprovalCode>6C4CF76F9D9DADF554F72FB77CF0417F</preApprovalCode>\r\n</payment>"
    headers = {
      'Content-Type': 'application/xml',
      'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
