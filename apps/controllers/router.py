from flask import Flask
from config import APPConfig
from apps.common.register import BlueprintRegister


app = Flask(__name__, template_folder=APPConfig.TEMPLATES_DIR, static_folder=APPConfig.STATIC_DIR)
app.config.from_object(APPConfig.from_app_mode())


BlueprintRegister(
    app=app,
    module_path=app.root_path.replace(f'{APPConfig.ROOT_DIR}/', '').replace('/', '.'),
    controllers_name=APPConfig.CONTROLLERS_MODULE_NAME
).register()


@app.route('/')
def index():
    return '200'

