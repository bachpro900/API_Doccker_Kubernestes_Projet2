import os
import requests
import time
import json

# définition de l'adresse de l'API
api_address = 'localhost'

# port de l'API
api_port = 8080

# requête1 | tester l'api!
payload = {
        "purchase_value": 200,
        "sex": True,
        "age": 40,
        "lead_time": 200,
        "source_Ads": True,
        "source_Direct": False,
        "source_SEO": False,
        "browser_Chrome": False,
        "browser_FireFox": True,
        "browser_IE": False,
        "browser_Opera": False,
        "browser_Safari": False
}

jload = json.dumps(payload)

requette = requests.get(
        url='http://{address}:{port}/api_test'.format(
            address=api_address, port=api_port),
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/json'
            },
        data=jload
        # params=payload
)

print(requette.status_code)

output = requette.content.decode('utf-8')
# json_obj = tmp # json.loads(tmp)
print(output)


# impression dans un fichier
if os.environ.get('LOG') and int(os.environ.get('LOG')) == 1:
    with open('api_test.log', 'a') as file:
        file.write(output)
time.sleep(1)

