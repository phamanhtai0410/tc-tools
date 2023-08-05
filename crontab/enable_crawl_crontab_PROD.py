import requests

headers = {
    'Authorization': 'rmNOMmLP4C0PI6DHkyyQ',
    'Content-Type': 'application/json'
}

requests.post('https://tc.dwf-labs.com/api/enable_crawl_flag', headers=headers)
