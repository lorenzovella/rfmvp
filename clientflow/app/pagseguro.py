import xml.etree.ElementTree as ET
import requests

token = '0E09DA92901245D895156260C19B1B8B'
email = 'lo2828@hotmail.com'

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

def aderirPlano(plano,referencia,user,hash):
    url = "https://ws.sandbox.pagseguro.uol.com.br/pre-approvals?email="+email+"&token="+token
    payload = {
    	"plan": plano,
    	"reference": referencia,
    	"sender": {
    		"name":  user.nome,
    		"email": user.email,
    		"hash": hash,
    		"phone": {
    			"areaCode": user.areatelefone,
    			"number": user.telefone
    		},
    		"address": {
    			"street": entrega,
    			"number": user.numero,
    			"complement": user.complemento,
    			"district": "It",
    			"city": user.cidade,
    			"state": user.estado,
    			"country": "BRA",
    			"postalCode": user.cep
    		},
    		"documents": [{
    			"type": "CPF",
    			"value": user.cpf
    		}]
    	},
    	"paymentMethod": {
    		"type": "CREDITCARD",
    		"creditCard": {
    			"token": hash,
    			"holder": {
    				"name": user.name,
    				"birthDate": user.nasimento,
    				"documents": [{
    					"type": "CPF",
    					"value": user.cpf
    				}],
    				"phone": {
    					"areaCode": user.telefone,
    					"number": user.areatelefone
    				},
    				"billingAddress": {
            			"street": user.rua,
            			"number": user.numero,
            			"complement": user.complemento,
            			"district": "It",
            			"city": user.cidade,
            			"state": user.estado,
            			"country": "BRA",
            			"postalCode": user.cep
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

def cobrarPlano(planoid,descricaoplano,valorplano,quantidadeplano,referencia,preaprovacao):
    url = "https://ws.sandbox.pagseguro.uol.com.br/pre-approvals/payment?email="+email+"&token="+token
    payload = {"<payment><items><item><id>"+planoid+"</id><description>"+descricaoplano+"</description><amount>"+valorplano+"</amount><quantity>"+quantidadeplano+"</quantity></item></items>reference>"+referencia+"</reference><preApprovalCode>"+preaprovacao+"</preApprovalCode></payment>"}
    headers = {
      'Content-Type': 'application/xml',
      'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
