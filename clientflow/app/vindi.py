import xml.etree.ElementTree as ET
import requests
import json
import os
tokenPublic = os.environ.get('vindipublic')
tokenPrivate = os.environ.get('vindiprivate')
vindiUrl = "https://app.vindi.com.br/api/v1/"

def buscarCliente(param):
    url = vindiUrl + "customers?query="+param['attribute']+":"+param['value']
    headers = {
      'Authorization': 'Basic '+tokenPrivate
    }
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)['customers']

def criarCliente(user):
    url = vindiUrl + "customers"
    payload = json.dumps({
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
      'Authorization': 'Basic '+tokenPrivate,
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    return json.loads(response.text)

def criarHash(nome,cpf,cn,cb,cvv,cem,cey):
    url = vindiUrl + "public/payment_profiles"
    payload = json.dumps({
      "holder_name": nome,
      "registry_code": cpf,
      "card_expiration": cem+"/"+cey,
      "allow_as_fallback": True,
      "card_number": cn,
      "card_cvv": cvv,
      "payment_method_code": "credit_card",
      "payment_company_code": "mastercard"
    })
    headers = {
      'Authorization': 'Basic '+tokenPublic,
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    return json.loads(response.text)

def criarAssinatura(clientVindi, hashVindi, planoVindi, produtosVindi):
    url = vindiUrl + "subscriptions"
    produtosArray = []
    for produto in produtosVindi:
        produtosArray.append(
            {
                "product_id": produto['id'],
                "quantity": produto['qtd'],
                "pricing_schema": {
                    "price": produto['valor'],
                    "schema_type": "per_unit"
                },
                "discounts": [
                {
                    "discount_type": "percentage",
                    "percentage": 50,
                    "quantity": 0,
                    "cycles": 1
                }
              ]
            })
    tempObject = {
        "plan_id": planoVindi,
        "customer_id": clientVindi,
        "payment_method_code": "credit_card",
        "product_items": produtosArray,
        "payment_profile": {
            "payment_company_code":"mastercard",
            "gateway_token": hashVindi
        }
    }

    payload = json.dumps( tempObject )
    headers = {
      'Authorization': 'Basic '+tokenPrivate,
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    return json.loads(response.text)

def buscarAssinatura(param):
    url = vindiUrl + "subscriptions?query="+param['attribute']+":"+param['value']
    headers = {
      'Authorization': 'Basic '+tokenPrivate
    }
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)['subscriptions'][0]
