from flask_script import Manager
from apps.controllers.router import app
from config import APPConfig


manager = Manager(app)


@manager.option('-h', '--host', dest='host', default=APPConfig.APP_HOST)
@manager.option('-p', '--port', dest='port', default=APPConfig.APP_PORT)
def runserver(host, port):
    app.run(host=host, port=port)

