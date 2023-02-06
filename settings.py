import os
from pathlib import Path

from dotenv import load_dotenv


dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

TOKEN = os.getenv("TOKEN")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
DB_NAME = os.getenv("DB_NAME")

ADMINS = []
for admin in os.getenv("ADMINS").split(";"):
    if admin:
        ADMINS.append(admin)
