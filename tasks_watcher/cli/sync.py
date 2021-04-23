from typing import List, Optional, Tuple

import typer
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from .database import database_path

sync_app = typer.Typer()

##### TODO #####


def create_drive():
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)


def upload_database_to_google_drive():
    drive = create_drive()
    upload_file_list = ["1.jpg", "2.jpg"]
    gfile = drive.CreateFile({"parents": [{"id": "1pzschX3uMbxU0lB5WZ6IlEEeAUE8MZ-t"}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(upload_file)
    gfile.Upload()  # Upload the file.


@tasks_app.command()
def upload():
    tasks = task_repository.list_all()
    typer.echo(f"[{task.id}] {task.name}")
