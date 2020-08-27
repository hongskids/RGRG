from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
import time
from datetime import datetime
import sys

crawlingTrigger = OrTrigger([CronTrigger(hour=9,minute=00), CronTrigger(hour=18,minute=00), CronTrigger(hour=14,minute=38)]) #오전 9시, 오후 6시에 한 번씩 크롤링

class Scheduler():
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()

    def __del__(self):
        print("Bye")
        self.shutdown()

    def kill_scheduler(self, job_id):
        try:
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            print("fail to stop scheduler : ", err)
            return

    def shutdown(self):
        self.sched.shutdown()

    #복지로 Page Crawling
    def bokjiroCrawling(self):
        try:
            f = open('CrawlingPage.py') #crawling 실행
            exec(f.read(), globals()) #globlas() - 전역변수 사용
            f.close()
        except Exception as ex:
            sys.exit("Error in scheduler bokjiro scheduler : ", ex)

    #정부24 API Crawling
    def api24(self):
        try:
            f = open('API24.py')  # 정부24 api crawling 실행
            exec(f.read(), globals())
            f.close()

        except Exception as ex:
            sys.exit("Error in scheduler bokjiro scheduler : ", ex)



    def scheduler(self, type):
        print("Scheduler Start", type)
        if type == 'cron':
            self.sched.add_job(self.bokjiroCrawling,crawlingTrigger)
            # self.sched.add_job(self.api24,crawlingTrigger)




scheduler = Scheduler()
scheduler.scheduler('cron')
now = datetime.now()
count = 0
while True:
    time.sleep(1)