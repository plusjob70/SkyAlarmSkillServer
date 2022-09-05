from config import DBConfig
from mongoengine import *
from models import *


class DBSession:
    def __init__(self):
        self.db = dict()

    def open(self, name):
        if name not in self.db:
            self.db[name] = connect('alarms', host=DBConfig.DB_URI, authentication_source='admin', alias='alarms')
        return self.db['name']

    def close(self, name):
        if name in self.db:
            disconnect(alias=name)


if __name__ == '__main__':
    print(DBConfig.DB_URI)

    alarms = connect(
        host=DBConfig.DB_URI,
        authentication_source='admin'
    )

    print(alarms)

