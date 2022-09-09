from config import DBConfig
from pymongo import MongoClient


client = MongoClient(host=DBConfig.DB_URI)
db = client.get_database(DBConfig.DB_NAME)

Routes = db.get_collection(DBConfig.COL_ROUTES)
Alarms = db.get_collection(DBConfig.COL_ALARMS)
Lowest = db.get_collection(DBConfig.COL_LOWEST)
Tickets = db.get_collection(DBConfig.COL_TICKETS)
