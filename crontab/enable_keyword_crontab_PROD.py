import requests

headers = {
    'Authorization': 'rmNOMmLP4C0PI6DHkyyQ',
    'Content-Type': 'application/json'
}
r = requests.put('https://tc.dwf-labs.com/api/analytics/vertical/keyword_url', headers=headers)
