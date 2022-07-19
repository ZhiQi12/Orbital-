from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from .scheduler import update_database

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_database, 'date', run_date='2022-7-19 13:04:05', name='update database', jobstore='default')
    scheduler.start()