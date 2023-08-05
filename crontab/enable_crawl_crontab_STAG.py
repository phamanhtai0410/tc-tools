import requests

headers = {
    'Authorization': 'rmNOMmLP4C0PI6DHkyyQ',
    'Content-Type': 'application/json'
}

requests.post('https://tc-api.esollabs.com/v1/tool/enable_crawl_flag', headers=headers)
