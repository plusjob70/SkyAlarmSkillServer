from flask import Blueprint, request
from apps.common.chatbot.response import ChatbotSkillResponse as Chatbot
from apps.common.chatbot.form import ChatbotReply, ChatbotContext
from apps.databases.session import Alarms
from apps.log.logger import logger
from apps.common.constants import DEFAULT_DATE, DATE_FORMAT
from datetime import datetime
from apps.common.exceptions import NotExistContext


app = Blueprint('apis_chatbot_skills', __name__, url_prefix='/apis/chatbot/skills')


@app.route('/select-route', methods=['POST'])
def select_route():
    data = request.json
    departure = data['action']['detailParams']['departure']['value']

    template = {
        'outputs': ChatbotReply.select_route_simple_text(),
        'quickReplies': ChatbotReply.select_route_quick_replies(departure)
    }

    return Chatbot.response(template=template)


@app.route('/select-date-age', methods=['POST'])
def select_date_and_age():
    data = request.json

    extra = data['action']['clientExtra']
    params = data['action']['detailParams']

    departure = extra.get('departure', '')
    destination = extra.get('destination', '')
    departure_date = params.get('departure_date', {}).get('origin', DEFAULT_DATE)
    age = params.get('age', {}).get('value', '')

    template = {
        'outputs': ChatbotReply.select_date_and_age_item_card(departure, destination, departure_date, age)
    }

    context = {
        'values': [ChatbotContext('alarm_info', 1,
                                  departure=departure, destination=destination,
                                  departure_date=departure_date, age=age).to_dict()]
    }

    return Chatbot.response(template=template, context=context)


@app.route('/register-alarm', methods=['POST'])
def register_alarm():
    data = request.json
    context = data['contexts']

    try:
        if not context or context[0]['name'] != 'alarm_info':
            raise NotExistContext

        params = context[0]['params']
        departure = params['departure']['value']
        destination = params['destination']['value']
        departure_date = params['departure_date']['value']
        age = params['age']['value']

        user_info = data['userRequest']
        user_id = user_info['user']['id']
        user_type = user_info['user']['type']
        user_timezone = user_info['timezone']

        results = Alarms.insert_one({
            'departure': departure,
            'destination': destination,
            'register_datetime': datetime.now(),
            'user_id': user_id,
            'user_type': user_type,
            'user_timezone': user_timezone,
            'departure_date': datetime.strptime(departure_date, DATE_FORMAT),
            'age': age
        })

        logger.info(f"[{user_id[:13]}] register-alarm : {departure} -> {destination} ({departure_date}) "
                    f"db.tickets._id: {results.inserted_id}")

        template = {
            'outputs': ChatbotReply.register_alarm_simple_text(succeed=True)
        }

    except (NotExistContext, KeyError) as e:
        logger.error(e)

        template = {
            'outputs': ChatbotReply.register_alarm_simple_text(succeed=False)
        }

    return Chatbot.response(template=template)


@app.route('/list-alarms', methods=['POST'])
def list_alarms():
    data = request.json
    user_id = data['userRequest']['user']['id']

    # alarms = col_alarms.find({
    #     'user_id': user_id,
    #     'departure_date': {'$gt': datetime.now().strftime(DATE_FORMAT)}
    # }).sort({
    #     'departure_date': 1
    # }).limit(ALARM_LIST_LIMIT)

    # print(alarms)
    #
    # logger.info(f"[{user_id[:13]}] list-alarms")
    #
    # template = {
    #     'outputs': ChatbotReply.list_alarms_carousel(alarms)
    # }

    return


@app.route('/delete-alarm', methods=['POST'])
def delete_alarm():
    return





