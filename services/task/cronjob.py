import requests
from config import Config

headers = {
    'Authorization': 'rmNOMmLP4C0PI6DHkyyQ',
    'Content-Type': 'application/json'
}
requests.post(f'{Config.API_URL}/output_list', headers=headers)