from flask import Blueprint, request
from typing import Optional
from pymongo.typings import _DocumentType
from apps.common.chatbot.response import ChatbotSkillResponse as Chatbot
from apps.common.chatbot.response import ChatbotResponseCode as Code
from apps.common.chatbot.form import ChatbotReply as Reply
from apps.common.chatbot.form import ChatbotContext as Context
from apps.databases.session import Alarms, Lowest
from apps.log.logger import logger
from apps.common.constants import DEFAULT_DATE, DATE_DASH_FORMAT, ALARM_LIST_LIMIT
from datetime import datetime
from apps.common.exceptions import (
    NotExistContext,
    ExceededAlarmCountLimit,
    NotExistObjectId,
    NotReadyYet
)
from bson.objectid import ObjectId
# from pprint import pprint


app = Blueprint('apis_chatbot_skills', __name__, url_prefix='/apis/chatbot/skills')


@app.route('/select-route', methods=['POST'])
def select_route():
    data = request.json
    departure = data['action']['detailParams']['departure']['value']

    template = {
        'outputs': Reply.select_route_simple_text(),
        'quickReplies': Reply.select_route_quick_replies(departure)
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

    template = {'outputs': Reply.select_date_and_age_item_card(departure, destination, departure_date, age)}

    context = {
        'values': [
            Context('alarm_info', 1,
                    departure=departure, destination=destination,
                    departure_date=departure_date, age=age).to_dict()
        ]
    }

    return Chatbot.response(template=template, context=context)


@app.route('/register-alarm', methods=['POST'])
def register_alarm():
    data = request.json
    context = data['contexts']

    try:
        if not context or context[0]['name'] != 'alarm_info':
            raise NotExistContext

        user_info = data['userRequest']
        user_id = user_info['user']['id']

        if Alarms.count_documents({'user_id': user_id}) >= ALARM_LIST_LIMIT:
            raise ExceededAlarmCountLimit

        user_type = user_info['user']['type']
        user_timezone = user_info['timezone']

        params = context[0]['params']
        departure = params['departure']['value']
        destination = params['destination']['value']
        departure_date = params['departure_date']['value']
        age = params['age']['value']

        results = Alarms.insert_one({
            'departure': departure,
            'destination': destination,
            'register_datetime': datetime.now(),
            'user_id': user_id,
            'user_type': user_type,
            'user_timezone': user_timezone,
            'departure_date': datetime.strptime(departure_date, DATE_DASH_FORMAT),
            'age': age
        })

        logger.info(f"[{user_id[:13]}] register-alarm : {departure} -> {destination} ({departure_date}) "
                    f"db.tickets._id: {results.inserted_id}")
        template = {'outputs': Reply.register_alarm_simple_text(Code.SUCCESS_INSERT)}

    except NotExistContext as e:
        logger.warning(e)
        template = {'outputs': Reply.register_alarm_simple_text(Code.NOT_EXIST_CONTEXT_ERROR)}

    except KeyError as e:
        logger.error(e)
        template = {'outputs': Reply.register_alarm_simple_text(Code.NOT_EXIST_ARGUMENT_ERROR)}

    except ExceededAlarmCountLimit as e:
        logger.warning(e)
        template = {'outputs': Reply.register_alarm_simple_text(Code.EXCEEDED_REGISTER_LIMIT)}

    return Chatbot.response(template=template)


@app.route('/list-alarms', methods=['POST'])
def list_alarms():
    data = request.json
    user_id = data['userRequest']['user']['id']

    logger.info(f"[{user_id[:13]}] list-alarms")
    alarms = Alarms.find({'user_id': user_id}).sort('departure_date')

    template = {'outputs': Reply.list_alarms_carousel(alarms)}

    return Chatbot.response(template=template)


@app.route('/delete-alarm', methods=['POST'])
def delete_alarm():
    data = request.json
    user_id = data['userRequest']['user']['id']
    extra = data['action']['clientExtra']

    try:
        alarm_id = extra['alarm_id']

        results = Alarms.delete_one({'_id': ObjectId(alarm_id)})

        if not results.deleted_count:
            raise NotExistObjectId

        logger.info(f"[{user_id[:13]}] delete-alarm : {alarm_id}")
        template = {'outputs': Reply.delete_alarm_simple_text(Code.SUCCESS_DELETE)}

    except NotExistObjectId:
        template = {'outputs': Reply.delete_alarm_simple_text(Code.ALREADY_DELETED_ERROR)}

    except KeyError:
        template = {'outputs': Reply.delete_alarm_simple_text(Code.NOT_EXIST_ARGUMENT_ERROR)}

    return Chatbot.response(template=template)


@app.route('/detail-alarm', methods=['POST'])
def detail_alarm():
    data = request.json
    user_id = data['userRequest']['user']['id']
    extra = data['action']['clientExtra']

    try:
        alarm_id: str = extra['alarm_id']
        lowest_id: str = extra['lowest_id']

        alarm: Optional[_DocumentType] = Alarms.find_one({'_id': ObjectId(alarm_id)})
        if not alarm:
            raise NotExistObjectId

        departure: str = alarm['departure']
        destination: str = alarm['destination']
        age: str = alarm['age']

        lowest: Optional[_DocumentType] = Lowest.find_one({'_id': lowest_id})
        if not lowest:
            raise NotReadyYet

        departure_datetime: datetime = lowest['departure_datetime']
        arrival_datetime: datetime = lowest['arrival_datetime']
        airline: str = lowest['airline']
        fee: int = lowest[age.lower()]
        seat_class: str = lowest['seat_class']

        logger.info(f"[{user_id[:13]}] detail-alarm : {alarm_id}")
        template = {
            'outputs': Reply.detail_alarm_item_card(
                departure, destination, age, departure_datetime, arrival_datetime, airline, fee, seat_class
            )
        }

    except NotReadyYet as e:
        logger.warning(f"[{user_id[:13]}] detail-alarm : {e}")
        template = {'outputs': Reply.detail_alarm_simple_text(Code.NOT_EXIST_LOWEST_WARNING)}

    except NotExistObjectId:
        template = {'outputs': Reply.detail_alarm_simple_text(Code.ALREADY_DELETED_ERROR)}

    except KeyError as e:
        logger.warning(f"[{user_id[:13]}] detail-alarm : {e}")
        template = {'outputs': Reply.detail_alarm_simple_text(Code.NOT_EXIST_ARGUMENT_ERROR)}

    return Chatbot.response(template=template)
