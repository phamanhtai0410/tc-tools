import requests
from crontab import CronTab

with CronTab(user='root') as cron:
    job = cron.new(command='python3 services/task/cronjob.py')
    job.day.every(1)
    
print('Writing ouput to db was just executed')