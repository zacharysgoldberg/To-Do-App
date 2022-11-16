from datetime import date
from fastapi import BackgroundTasks
from utils.send_email import send_email
from apscheduler.schedulers.blocking import BlockingScheduler


def reminder(todo_date: str, email: str, todo_title: str):
    msg = f'Hello, {email} This is a reminder that your todo, "{todo_title}" is today.'

    schedule = BlockingScheduler()
    schedule.add_job(send_email, 'date', run_date=f"{todo_date}",
                     args=['Reminder', [email], msg])
    print("==========================")
    schedule.start()
    print("==========================")
