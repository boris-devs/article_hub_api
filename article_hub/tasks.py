import csv
import os

from celery import shared_task

from article_hub.settings import PATH_LOG_CSV_FILE
from users.models import User

@shared_task
def register_user_log(user: User):
    file_exists = os.path.exists(PATH_LOG_CSV_FILE)

    print(f"Welcome {user.email}!")

    with open(PATH_LOG_CSV_FILE, "a", newline="") as file:
        fieldnames = ["_id", "email", "username", "first_name", "last_name", "date_joined"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)


        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "_id": user._id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined
        })
