from flet import *
from user_table import create_table

import sqlite3
conn = sqlite3.connect("db/userdb.db", check_same_thread=False)