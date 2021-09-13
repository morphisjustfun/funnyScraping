import http.client
import os
import sys
import json

conn = http.client.HTTPSConnection("consultas-api.pongoelhombro.gob.pe")
payload = {'documento': sys.argv[3], 'tipoDocumento': '1', 'nacionalidad':''}
payload = json.dumps(payload)
headers = {
  'GAction': f'{sys.argv[1]}',
  'Accept': 'application/json, text/plain, */*',
  'Content-Type': 'application/json',
  'GResponse': f'{sys.argv[2]}',
  'sec-ch-ua-mobile': '?0',
  'origin':'https://consultas.pongoelhombro.gob.pe',
  'referer':"https://consultas.pongoelhombro.gob.pe/",
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90"'
}
conn.request("POST", "/ciudadano", payload, headers)
res = conn.getresponse()
if res.status != 200:
    exit(1)
else:
    data = res.read()
    print(data.decode('utf-8'))
