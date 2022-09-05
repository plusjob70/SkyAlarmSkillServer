from mongoengine.context_managers import *
import mongoengine
from flask import Blueprint, request
from apps.common.response import ChatbotSkillResponse as Chatbot
from apps.common.chatbot.replies import ChatbotReply
from apps.databases.models import Alarm
from apps.log.logger import logger
from apps.common.constants import DEFAULT_DATE, DATETIME_FORMAT, DATE_FORMAT, ALARM_LIST_LIMIT
from datetime import datetime
from pprint import pprint
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
        'values': [{
            'name': 'alarm_info',
            'lifeSpan': 1,
            'params': {
                 'departure': departure,
                 'destination': destination,
                 'departure_date': departure_date,
                 'age': age
            }
        }]
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

        logger.info(f"[{user_id[:13]}] register-alarm : {departure} -> {destination} ({departure_date})")

        with switch_collection(Alarm, 'alarms') as alarm:
            alarm(
                register_datetime=datetime.now(),
                user_id=user_id,
                user_type=user_type,
                user_timezone=user_timezone,
                departure=departure,
                destination=destination,
                departure_date=datetime.strptime(departure_date, DATE_FORMAT),
                age=age
            ).save()


        # Alarm(
        #     register_datetime=datetime.now(),
        #     user_id=user_id,
        #     user_type=user_type,
        #     user_timezone=user_timezone,
        #     departure=departure,
        #     destination=destination,
        #     departure_date=datetime.strptime(departure_date, DATE_FORMAT),
        #     age=age
        # ).save()

        template = {
            'outputs': ChatbotReply.register_alarm_simple_text(remain=True)
        }

    except (mongoengine.connection.ConnectionFailure, NotExistContext) as e:
        logger.error(e)

        template = {
            'outputs': ChatbotReply.register_alarm_simple_text(remain=False)
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





