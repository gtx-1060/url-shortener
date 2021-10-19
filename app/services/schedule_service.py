from datetime import datetime

from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from app.data.db.db import SQLALCHEMY_DATABASE_URL
from app.exceptions import BaseHTTPException


class _MyScheduler:
    __scheduler: AsyncIOScheduler

    def __init__(self):
        jobstores = {
            'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URL, tablename="apschedulers_table")
        }
        executors = {
            'default': ThreadPoolExecutor()
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 2
        }
        self.__scheduler = AsyncIOScheduler()
        self.__scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults,
                                   timezone=timezone('Europe/Moscow'))

    def start(self):
        self.__scheduler.start()

    def stop(self):
        self.__scheduler.shutdown()

    def plan_task(self, task_id: str, date: datetime, task_func, f_args: list, misfire_times=3600):
        try:
            self.__scheduler.add_job(id=task_id, trigger='date', func=task_func, run_date=date, args=f_args,
                                     misfire_grace_time=misfire_times)
        except Exception as e:
            print(e)
            raise BaseHTTPException(500, "Cannot schedule task")

    def plan_periodic_task(self, task_id: str, interval_seconds, task_func, f_args: list):
        try:
            self.__scheduler.add_job(id=task_id, trigger='interval', seconds=interval_seconds, func=task_func, args=f_args)
        except Exception as e:
            print(e)
            raise BaseHTTPException(500, "Cannot schedule task")

    def replan_task(self, task_id: str, date: datetime):
        try:
            self.__scheduler.modify_job(task_id, run_date=date)
        except Exception as e:
            print(e)
            raise BaseHTTPException(500, "Cannot schedule task")

    def remove_task(self, task_id: str):
        try:
            self.__scheduler.remove_job(task_id)
        except Exception as e:
            print(e)
            raise BaseHTTPException(500, "Cannot remove scheduled task")

    def task_exists(self, task_id: str) -> bool:
        jobs = self.__scheduler.get_jobs()
        for job in jobs:
            if job.id == task_id:
                return True
        return False


myscheduler = _MyScheduler()
