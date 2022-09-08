from config import DBConfig
from pymongo import MongoClient
from apps.common.chatbot.skill_template import *
from pprint import pprint


client = MongoClient(host=DBConfig.DB_URI)
db = client.get_database(DBConfig.DB_NAME)

Routes = db.get_collection(DBConfig.COL_ROUTES)
Alarms = db.get_collection(DBConfig.COL_ALARMS)
Lowest = db.get_collection(DBConfig.COL_LOWEST)
Tickets = db.get_collection(DBConfig.COL_TICKETS)


if __name__ == '__main__':
    user_id = 'aa1b537ebd464841c42718d7bf760c3a16be29ca080171f4e89a9a0ea3ca10d165'
    alarms = Alarms.find({'user_id': user_id}).sort('departure_date')

    for al in alarms:
        print(str(al['_id']))
