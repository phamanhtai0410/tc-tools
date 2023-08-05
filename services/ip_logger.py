

from models import IpLogsModel
from lib.utils import dt_utcnow
from flask import request
from pydash import get
import datetime
from config import Config
from telegram import Bot
from pymongo.mongo_client import MongoClient
import asyncio
async def send_message_async(token, chat_id, text):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=text)

def send_message(token, chat_id, text):
    asyncio.run(send_message_async(token, chat_id, text))
class IpLoggerService:
    
    @staticmethod
    def log_new_request():
        ip = get(request.headers, 'X-Real-IP')
        print('Logging request ip : ', ip)
        if not ip:
            return {}
        _IP = Config.IP
        print(_IP)
        if ip in _IP:
            
            IpLogsModel.update_one(
                    filter={
                        'ip': ip
                    },
                    obj={
                        'updated_by': 'services:IpLoggerService:update_ip_log'
                    }
                
            )
        # _check = IpLogsModel.find_one(
        #     filter={
        #         'ip': ip
        #     }
        # )
        # if not _check:
        #     IpLogsModel.insert_one(
        #         {
        #             'ip': ip,
        #             'created_by': 'services:IpLoggerService:insert_ip_log',
        #         }
        #     )
        # else:    
        #     IpLogsModel.update_one(
        #         filter={
        #             'ip': ip
        #         },
        #         obj={
        #             'updated_by': 'services:IpLoggerService:update_ip_log'
        #         }
                
        #     )
        return {}
    @staticmethod
    def check_ip():
        now = datetime.datetime.now()
        six_hour_ago = now - datetime.timedelta(hours=6)
        cursor = IpLogsModel.find(filter={'deleted': False, 'updated_time': {'$lt': six_hour_ago}},projection={'ip':1,'updated_time':1})
        # total = IpLogsModel.count_documents(filter={'deleted': False, 'updated_time': {'$lt': six_hour_ago}})
        ip_string = ""
        i = 0
        for document in cursor:
            i+=1
            ip_string += 'IP: ' + document['ip'] + ' = > '
            ip_string += 'Last time: ' + document['updated_time'].strftime("%Y-%m-%d %H:%M:%S") + '\n'
        ip_string+='\nTotal: '+str(i)+ '\n' + '======================================'
        send_message(Config.BOT_API,Config.CHAT_ID,ip_string)
