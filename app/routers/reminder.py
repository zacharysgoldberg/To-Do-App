from datetime import date
from utils.send_email import send_email
from apscheduler.schedulers.background import BackgroundScheduler


def reminder(todo_date: str, email: str, todo_title: str, background_tasks):
    msg = f'Hello, {email} This is a reminder that your todo, "{todo_title}" is today.'

    schedule = BackgroundScheduler()
    schedule.add_job(send_email, 'date', next_run_time=todo_date,
                     args=['Reminder', [email], msg, background_tasks])
    schedule.start()
