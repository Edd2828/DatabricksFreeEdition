from credentials import username, password, security_token, consumer_key, consumer_secret, client_id, client_secret, email
from simple_salesforce import Salesforce

sf = Salesforce(
    username=username, 
    password=password, 
    security_token=security_token,
    domain='login'
    )

response = sf.query("select Name, Rating, CreatedDate from Account")

print(sf)

sf = Salesforce(
    username=username, 
    password=password,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret # for most dev orgs; see note below
)

# Your SOQL query
response = sf.query("select Name, Rating, CreatedDate from Account")

print(response)

import requests

DOMAIN = "https://orgfarm-0185455700-dev-ed.develop.lightning.force.com/"

payload = {
    'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': email,
    'password': password
}
oauth_endpoint = '/services/oauth2/token'

DOMAIN = "https://orgfarm-0185455700-dev-ed.develop.my.salesforce.com/services/oauth2/token"
# HEADER = {'Content-Type': 'application/x-www-form-urlencode'}
PARAMS = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'api'
}

response = requests.post(url=DOMAIN, data=PARAMS)
print(response.status_code)



