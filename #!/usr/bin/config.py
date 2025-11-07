# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x]
DATABASE_PATH = 'maps_bot_database.db'
