from database.connector import Database
from config import Configuration


db = Database(
    dbname=Configuration.DB_NAME,
    user=Configuration.DB_USER,
    password=Configuration.DB_PASS,
    host=Configuration.DB_HOST
)
