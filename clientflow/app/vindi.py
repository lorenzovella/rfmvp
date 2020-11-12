import xml.etree.ElementTree as ET
import requests
import json
import os
tokenPublic = os.environ.get('vindipublic')
tokenPrivate = os.environ.get('vindiprivate')
vindiUrl = "https://sandbox-app.vindi.com.br/api/v1/"

def criarCliente(user):
    url = vindiUrl + "customers"
    payload = json.dumps(
    {
      "name": user.nome,
      "email": user.email,
      "registry_code": user.cpf,
      "code": user.id,
      "address": {
		"street": user.rua,
		"number": user.numero,
        "additional_details": user.complemento,
        "zipcode": user.cep,
        "neighborhood": user.bairro,
        "city": user.cidade,
        "state": user.estado,
        "country": "BR"
      },
      "phones": [
        {
          "phone_type": "mobile",
          "number": "55" + str(user.areatelefone) + str(user.telefone),
          "extension": ""
        }
      ]
    })
    headers = {
      'Authorization': 'Basic '+'SkR4WmVSMHJrMzdoTVRqTlpYWlZfeGtrdU4wRjVxRUs1elc0V2NaVXk2RTo=',
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    return json.loads(response.text)

def criarSession():
    url = vindiUrl + "/v2/sessions?email="+email+"&token="+token
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

def aderirPlano(plano,referencia,hash,cardHolder,user,ip):
    url = vindiUrl + "/pre-approvals?email="+email+"&token="+token
    payload = json.dumps({
    	"plan": plano,
    	"reference": referencia,
    	"sender": {
    		"name":  user.nome,
    		"email": user.email,
    		"ip": ip,
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
    url = vindiUrl + "/pre-approvals/payment?email="+email+"&token="+token
    payload = "<payment><items><item><id>"+planoid+"</id><description>"+descricaoplano+"</description><amount>"+valorplano+"</amount><quantity>"+quantidadeplano+"</quantity></item></items><reference>"+referencia+"</reference><preApprovalCode>"+preaprovacao+"</preApprovalCode></payment>"
    headers = {
      'Content-Type': 'application/xml',
      'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
    }
    response = requests.request("POST", url, headers=headers, data = payload)


def consultaAssinatura(codigoAdesao):
    url = vindiUrl + "/pre-approvals/"+codigoAdesao+"?email="+email+"&token="+token
    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    print(response)
    jsonResponse = json.loads(response.text)
    if 'status' in jsonResponse:
        return statusAssinatura[jsonResponse['status']]
    else:
        return jsonResponse['errors']


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

def listaPagamentos(codigoAdesao):
    url = vindiUrl + "/pre-approvals/"+codigoAdesao+"/payment-orders?email="+email+"&token="+token
    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    jsonResponse = json.loads(response.text)
    return jsonResponse['paymentOrders']

def suspendePlano(codigoAdesao):
    url = vindiUrl + "/pre-approvals/"+codigoAdesao+"/status?email="+email+"&token="+token

    payload = "{\n\t\"status\":\"SUSPENDED\"\n}"
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
    }

    response = requests.request("PUT", url, headers=headers, data = payload)
    if response.status_code == 204:
        return "Pronto! seu plano foi suspenso."
    else:
        jsonResponse = json.loads(response.text)
        return "Houve um erro!" + str(jsonResponse['errors'])

def cancelaPlano(codigoAdesao):
    url = vindiUrl + "/pre-approvals/"+codigoAdesao+"/cancel?email="+email+"&token="+token

    payload  = {}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
    }

    response = requests.request("PUT", url, headers=headers, data = payload)
    if response.status_code == 204:
        return "Pronto! seu plano foi Cancelado."
    else:
        jsonResponse = json.loads(response.text)
        return "Houve um erro!" + str(jsonResponse['errors'])

def descontoPlano(codigoAdesao, novoValor):
    url = vindiUrl + "/pre-approvals/request/"+codigoAdesao+"/payment?email="+email+"&token="+token

    payload = "{\r\n  \"amountPerPayment\": \""+novoValor+"\",\r\n  \"updateSubscriptions\": true\r\n}"
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
    }

    response = requests.request("PUT", url, headers=headers, data = payload)
    if response.status_code != 204:
        raise Exception("Erro ao aplicar cupom")
    return True
