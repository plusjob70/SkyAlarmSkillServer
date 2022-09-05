from flask import Blueprint


app = Blueprint('apis', __name__, url_prefix='/apis')


@app.route('/')
def index():
    return 'hello'

