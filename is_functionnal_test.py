import os
import requests
import time

#définition de l'adresse de l'API
api_address = 'localhost'

# port de l'API
api_port = 8080

# requête1
requette = requests.get(
        url='http://{address}:{port}/'.format(address=api_address, port=api_port)
    
)


output = '''
============================
    API functionnal test
============================

request done at "/"

expected result = 200
actual restult = {status_code}

==>  {test_status}

'''

# statut de la requête
status_code = requette.status_code

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))


#impression dans un fichier
if int(os.environ.get('LOG')) == 1:
    with open('api_test.log', 'a') as file:
        file.write(output)
time.sleep(2)
