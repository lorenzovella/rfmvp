import xml.etree.ElementTree as ET
import requests
import json
import os
token = os.environ.get('pgtoken')
email = os.environ.get('pgemail')

def criarPlano(name,reference,valor):
    url = "https://ws.pagseguro.uol.com.br/pre-approvals/request/?email="+email+"&token="+token
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
    url = "https://ws.pagseguro.uol.com.br/v2/sessions?email="+email+"&token="+token
    payload = {}
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    session = ET.fromstring(response.text)[0].text
    return session

def criarHash(session,valor,cn,cb,cvv,cem,cey):
    url = "https://df.uol.com.br/v2/cards"
    payload = 'sessionId='+session+'&amount='+valor+'&cardNumber='+cn+'&cardBrand='+cb+'&cardCvv='+cvv+'&cardExpirationMonth='+cem+'&cardExpirationYear='+cey
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    hash = ET.fromstring(response.text)[0].text
    return hash

def aderirPlano(plano,referencia,hash,cardHolder,user):
    url = "https://ws.pagseguro.uol.com.br/pre-approvals?email="+email+"&token="+token
    payload = json.dumps({
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
    			"street": user.rua,
    			"number": user.numero,
    			"complement": user.complemento,
    			"district": user.bairro,
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
    				"name": cardHolder,
    				"birthDate": user.nascimento.strftime('%d/%m/%Y'),
    				"documents": [{
    					"type": "CPF",
    					"value": user.cpf
    				}],
    				"phone": {
    					"areaCode": user.areatelefone,
    					"number": user.telefone
    				},
    				"billingAddress": {
            			"street": user.rua,
            			"number": user.numero,
            			"complement": user.complemento,
            			"district": user.bairro,
            			"city": user.cidade,
            			"state": user.estado,
            			"country": "BRA",
            			"postalCode": user.cep
    				}
    			}
    		}
    	}
    }, default=str)
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.pagseguro.com.br.v1+json;charset=ISO-8859-1'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    jsonResponse = json.loads(response.text)
    if 'code' in jsonResponse:
        return jsonResponse['code']
    else:
        return jsonResponse['errors']

def cobrarPlano(planoid,descricaoplano,valorplano,quantidadeplano,referencia,preaprovacao):
    url = "https://ws.pagseguro.uol.com.br/pre-approvals/payment?email="+email+"&token="+token
    payload = "<payment><items><item><id>"+planoid+"</id><description>"+descricaoplano+"</description><amount>"+valorplano+"</amount><quantity>"+quantidadeplano+"</quantity></item></items><reference>"+referencia+"</reference><preApprovalCode>"+preaprovacao+"</preApprovalCode></payment>"
    headers = {
      'Content-Type': 'application/xml',
      'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
    }
    response = requests.request("POST", url, headers=headers, data = payload)


def consultaAssinatura(codigoAdesao):
    url = "https://ws.pagseguro.uol.com.br/pre-approvals/"+codigoAdesao+"?email="+email+"&token="+token
    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    jsonResponse = json.loads(response.text)
    if 'status' in jsonResponse:
        return statusAssinatura[jsonResponse['status']]


statusAssinatura = {
  "INITIATED" : "O comprador iniciou o processo de pagamento, mas abandonou o checkout e não concluiu a compra.",
  "PENDING" : "O processo de pagamento foi concluído e transação está em análise ou aguardando a confirmação da operadora.",
  "ACTIVE" : "A criação da recorrência, transação validadora ou transação recorrente foi aprovada.",
  "PAYMENT_METHOD_CHANGE" : "Uma transação retornou como \"Cartão Expirado, Cancelado ou Bloqueado\" e o cartão da recorrência precisa ser substituído pelo comprador.",
  "SUSPENDED" : "A recorrência foi suspensa pelo vendedor.",
  "CANCELLED" : "A criação da recorrência foi cancelada pelo PagSeguro",
  "CANCELLED_BY_RECEIVER" : "A recorrência foi cancelada a pedido do vendedor.",
  "CANCELLED_BY_SENDER" : "A recorrência foi cancelada a pedido do comprador.",
  "EXPIRED" : "A recorrência expirou por atingir a data limite da vigência ou por ter atingido o valor máximo de cobrança definido na cobrança do plano."
  }
