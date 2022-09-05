from flask import Blueprint, request
from apps.common.chatbot.response import ChatbotParamValidResponse


app = Blueprint('apis_chatbot_validate', __name__, url_prefix='/apis/chatbot/validate')


@app.route('/lines', methods=['POST'])
def validate_lines():
    print(request.json)

    data = request.json
    try:
        destination = data['value']['resolved']

    except KeyError:
        ...

    return ChatbotParamValidResponse.fail()



"""
{
    'bot': {
        'id': '62dde66ac7d05102c2cd00a7!', 
        'name': '알람봇'
    }, 
    'utterance': '202020\n', 
    'params': {
        'surface': 'BuilderBotTest', 
        'ignoreMe': 'true'
    }, 
    'isInSlotFilling': True, 
    'user': {
        'id': 'aadbc134c8b80e823bd18d31e4650eebe29ca080171f4e89a9a0ea3ca10d165', 
        'type': 'botUserKey', 
        'properties': {
            'botUserKey': 'aadbcb1c134c8b80e823bd18d31e4650eebe29ca080171f4e89a9a0ea3ca10d165', 
            'bot_user_key': 'aadbcb1c134c8b80e823bd18d31e4650eebe29ca080171f4e89a9a0ea3ca10d165'
        }
    }, 
    'value': {
        'origin': '202020', 
        'resolved': '202020'
    }, 
    'timezone': 'Asia/Seoul', 
    'lang': 'kr'
}
"""