from apps.common.chatbot.blocks import *
from apps.common.airports import KOR_AIRPORTS
from apps.common.lines import LINES
from dictionary import Age


class ChatbotContext:
    def __init__(self, name, life, **params):
        self.name = name
        self.lifeSpan = life
        self.params = params

    def to_dict(self) -> dict:
        return vars(self)


class ChatbotReply:
    @staticmethod
    def select_route_simple_text() -> list[dict]:
        return [{'simpleText': {'text': '도착지를 선택해주세요.'}}]

    @staticmethod
    def select_route_quick_replies(departure: str) -> list[dict]:
        return [{
            'label': KOR_AIRPORTS[destination]['location'],
            'messageText': KOR_AIRPORTS[destination]['location'],
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
                        'description': f"{KOR_AIRPORTS[departure]['location']} ▶ "
                                       f"{KOR_AIRPORTS[destination]['location']}"
                    },
                    {
                        'title': '출발',
                        'description': f"{KOR_AIRPORTS[departure]['simple_name']} ({departure})"
                    },
                    {
                        'title': '도착',
                        'description': f"{KOR_AIRPORTS[destination]['simple_name']} ({destination})"
                    },
                    {
                        'title': '출발 날짜',
                        'description': f'{departure_date}'
                    },
                    {
                        'title': '연령',
                        'description': f'{Age.CHILD.kor if age==Age.CHILD.eng else Age.ADULT.kor}'
                    },
                    {
                        'title': '알림 주기',
                        'description': '매일 09시경'
                    }
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
                        'messageText': '아니요',
                        'blockId': MAIN_EXIT_BLOCK
                    }
                ],
                'buttonLayout': 'horizontal'
            }
        }]

    @staticmethod
    def register_alarm_simple_text(succeed: bool) -> list[dict]:
        return [{
            'simpleText': {
                'text': '등록을 성공하였습니다.' if succeed
                else '등록에 실패하였습니다.\n처음부터 다시 진행해주세요.'
            }
        }]

    @staticmethod
    def list_alarms_carousel(alarms) -> list[dict]:
        return [{
            'carousel': {
                'type': 'itemCard',
                'items': [
                    {
                        'title': '',
                        'description': '',
                        'itemList': [
                            {
                                'title': '노선',
                                'description': f"{alarm} ▶ "
                                               f"{alarm}"
                            },
                            {
                                'title': '출발',
                                'description': f"{alarm} ({alarm})"
                            },
                            {
                                'title': '도착',
                                'description': f"{alarm} ({alarm})"
                            },
                            {
                                'title': '출발 날짜',
                                'description': f'{alarm}'
                            },
                            {
                                'title': '연령',
                                'description': f'{alarm}'
                            },
                            {
                                'title': '알림 주기',
                                'description': '매일 09시경'
                            },
                            {
                                'title': '최저가',
                                'description': '0원'
                            }
                        ],
                        'itemListAlignment': 'right',
                        'buttons': [
                            {
                                'label': '삭제',
                                'action': 'block',
                                'blockId': '',
                            },
                        ],
                    }
                    for alarm in alarms]
            }
        }]

