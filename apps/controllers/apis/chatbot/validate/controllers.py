from flask import Blueprint, request
from apps.common.chatbot.response import ChatbotParamValidResponse
from apps.common.constants import DATE_DASH_FORMAT, DEFAULT_DATE
from datetime import datetime, date


app = Blueprint('apis_chatbot_validate', __name__, url_prefix='/apis/chatbot/validate')


@app.route('/departure_date', methods=['POST'])
def validate_departure_date():
    data: dict = request.json

    departure_date_str: str = data.get('value', {}).get('origin', DEFAULT_DATE)
    departure_date: date = datetime.strptime(departure_date_str, DATE_DASH_FORMAT).date()

    delta: int = (departure_date - datetime.now().date()).days

    if delta < 2:
        return ChatbotParamValidResponse.fail()
    return ChatbotParamValidResponse.ok()
