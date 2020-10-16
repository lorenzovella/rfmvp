import requests
import json
import os
import requests

key = os.environ.get('rdtoken')

def criarLead(cliente, pedido):

    url = "https://api.rd.services/platform/conversions?api_key="+key
    payload = json.dumps({
    "event_type": "CONVERSION",
    "event_family": "CDP",
    "payload": {
        "conversion_identifier":pedido,
        "name":str(cliente.nome+" "+cliente.sobrenome),
        "email": cliente.email,
        "state": cliente.estado,
        "city": cliente.cidade,
        "country": "BR",
        "mobile_phone": str(cliente.areatelefone+cliente.telefone),
        "available_for_mailing": True,
        }
    }, default=str)

    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    return(response.text.encode('utf8'))
