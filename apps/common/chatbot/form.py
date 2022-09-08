from apps.common.chatbot.response import ChatbotResponseCode as Code
from apps.common.chatbot.blocks import *
from apps.common.lines import LINES
from apps.common.constants import *
from dictionary import Age, Airports, Airlines
from apps.common.chatbot.skill_template import *
from datetime import datetime


class ChatbotContext:
    def __init__(self, name: str, life: int, **params: dict):
        self.name = name
        self.lifeSpan = life
        self.params = params

    def to_dict(self) -> dict:
        return self.__dict__


class ChatbotReply:
    @staticmethod
    def select_route_simple_text() -> list[dict]:
        return [{'simpleText': {'text': '도착지를 선택해주세요.'}}]

    @staticmethod
    def select_route_quick_replies(departure: str) -> list[dict]:
        return [{
            'label': Airports[destination].location,
            'messageText': Airports[destination].location,
            'action': 'block',
            'blockId': REGISTER_SELECT_DATE_AND_AGE_BLOCK,
            'extra': {
                'departure': departure,
                'destination': destination
            }
        } for destination in LINES[departure]]

    @staticmethod
    def select_date_and_age_item_card(
            departure: str, destination: str,
            departure_date: str, age: str
    ) -> list[dict]:
        return [{
            'itemCard': {
                "imageTitle": {
                    "title": "등록 진행",
                    "description": "아래 내용으로 최저가알림 등록을 진행합니다."
                },
                'title': '',
                'description': '',
                'itemList': [
                    {
                        'title': '노선',
                        'description': f"{Airports[departure].location} ▶ {Airports[destination].location}"
                    },
                    {
                        'title': '출발',
                        'description': f"{Airports[departure].full_name} ({departure})"
                    },
                    {
                        'title': '도착',
                        'description': f"{Airports[destination].full_name} ({destination})"
                    },
                    {
                        'title': '출발 날짜',
                        'description': f'{departure_date}'
                    },
                    {
                        'title': '연령',
                        'description': f'{Age.CHILD.kor if age == Age.CHILD.eng else Age.ADULT.kor}'
                    },
                ],
                'itemListAlignment': 'right',
                'buttons': [
                    {
                        'label': '네',
                        'action': 'block',
                        'blockId': REGISTER_ALARM_BLOCK,
                    },
                    {
                        'label': '아니요',
                        'action': 'block',
                        'blockId': MAIN_EXIT_BLOCK
                    }
                ],
                'buttonLayout': 'horizontal'
            }
        }]

    @staticmethod
    def register_alarm_simple_text(code: int) -> list[dict]:
        match code:
            case Code.SUCCESS_INSERT:
                text = '등록을 성공하였습니다.'
            case Code.EXCEEDED_REGISTER_LIMIT:
                text = '알림 등록 개수를 초과하여 등록에 실패했습니다.'
            case Code.NOT_EXIST_ARGUMENT_ERROR | Code.NOT_EXIST_CONTEXT_ERROR:
                text = '비정상적인 접근으로 등록에 실패했습니다.'
            case _:
                text = ''

        return [{'simpleText': {'text': text}}]

    @staticmethod
    def list_alarms_carousel(alarms: list) -> list[Carousel]:
        return [
            Carousel(
                type='itemCard',
                items=[
                    Item(
                        title='',
                        description='',
                        itemList=[
                            Obj(title='노선',
                                description=f"{Airports[alarm['departure']].location} ▶ "
                                            f"{Airports[alarm['destination']].location}"),
                            Obj(title='출발',
                                description=f"{Airports[alarm['departure']].full_name} ({alarm['departure']})"),
                            Obj(title='도착',
                                description=f"{Airports[alarm['destination']].full_name} ({alarm['destination']})"),
                            Obj(title='출발 날짜',
                                description=f"{alarm['departure_date'].strftime(DATE_DASH_FORMAT)}"),
                            Obj(title='연령',
                                description=f"{Age[alarm['age']].kor}")
                        ],
                        itemListAlignment='right',
                        buttons=[
                            Button(label='자세히 보기', action='block', blockId=DETAIL_DETAIL_ALARMS_BLOCK,
                                   extra=Obj(
                                       alarm_id=str(alarm['_id']),
                                       lowest_id=f"{alarm['departure_date'].strftime(DATE_JOIN_FORMAT)}"
                                                 f"{alarm['departure']}"
                                                 f"{alarm['destination']}"
                                   )),
                            Button(label='삭제', action='block', blockId=DETAIL_DELETE_ALARM_BLOCK,
                                   extra=Obj(alarm_id=str(alarm['_id'])))
                        ]
                    )
                    for alarm in alarms]
            )
        ]

    @staticmethod
    def delete_alarm_simple_text(code: int) -> list[SimpleText]:
        match code:
            case Code.SUCCESS_DELETE:
                text = '삭제하였습니다.'
            case Code.ALREADY_DELETED_ERROR:
                text = '이미 삭제된 알림입니다.'
            case Code.NOT_EXIST_ARGUMENT_ERROR:
                text = '비정상적인 접근으로 등록에 실패했습니다.'
            case _:
                text = ''

        return [SimpleText(text=text)]

    @staticmethod
    def detail_alarm_item_card(departure: str, destination: str, age: str,
                               departure_datetime: datetime, arrival_datetime: datetime,
                               airline: str, fee: int, seat_class: str) -> list[ItemCard]:
        return [
            ItemCard(
                title=f"{departure} ▶ {destination}",
                destination='',
                itemList=[
                    Obj(title='출발', description=f"{Airports[departure].full_name} ({departure})"),
                    Obj(title='도착', description=f"{Airports[destination].full_name} ({destination})"),
                    Obj(title='출발 날짜', description=f"0000-00-00"),
                    Obj(title='출발', description=f"{departure_datetime}"),
                    Obj(title='도착', description=f"{arrival_datetime}"),
                    Obj(title='항공사', description=f"{Airlines[airline].kor_name}"),
                    Obj(title='좌석등급', description=seat_class),
                    Obj(title='연령', description=Age[age].kor)
                ],
                itemListAlignment='right',
                itemListSummary=Obj(title='요금', description='{:,}원'.format(fee)),
                buttons=[
                    Button(label='btn1', action=''),
                    Button(label='btn2', action='', blockId='')
                ],
                buttonLayout='horizontal'
            )
        ]

    @staticmethod
    def detail_alarm_simple_text(code: int) -> list[SimpleText]:
        match code:
            case Code.ALREADY_DELETED_ERROR | Code.NOT_EXIST_ARGUMENT_ERROR:
                text = '존재하지 않는 알림입니다.'
            case _:
                text = ''

        return [SimpleText(text=text)]

