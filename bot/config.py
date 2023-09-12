from dotenv import load_dotenv

import os

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
SHOP_ID = os.environ.get("SHOP_ID")
SHOP_API_TOKEN = os.environ.get("SHOP_API_TOKEN")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
