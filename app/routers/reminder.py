from fastapi.responses import HTMLResponse
from todos import router
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler
import os


@router.post('/reminder', response_class=HTMLResponse)
async def send_reminder():
    return


def reminder(todo_date: str, email: str, todo_title: str):
    message = """
        <!DOCTYPE html>
        <html>
        <title>Reminder</title>
        <div style="width:100%;font-family: monospace;">
            <h2>Hello, {0:}</h2>
            <p>This is a reminder that your todo "{1:}" is today.</p>
        </div>
        </html>
        """.format(email, todo_title)

    schedule = BlockingScheduler()

    schedule.add_job(message, 'date', run_date=date(todo_date), args=['text'])

    schedule.start()
