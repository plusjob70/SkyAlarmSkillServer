from enum import Enum


class Age(Enum):
    ADULT = ('성인', 'adult')
    CHILD = ('아동', 'child')

    def __init__(self, kor, eng):
        self.kor = kor
        self.eng = eng
