import requests

headers = {
    'Authorization': 'rmNOMmLP4C0PI6DHkyyQ',
    'Content-Type': 'application/json'
}
r = requests.put('https://tc-api.esollabs.com/v1/tool/analytics/vertical/keyword_url', headers=headers)
print(r.text)