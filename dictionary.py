from enum import Enum


class Age(Enum):
    ADULT = ('성인', 'adult')
    CHILD = ('아동', 'child')

    def __init__(self, kor, eng):
        self.kor = kor
        self.eng = eng


class Airports(Enum):
    GMP = ('GMP', '김포공항', '김포국제공항', '서울')
    ICN = ('ICN', '인천공항', '인천국제공항', '인천')
    PUS = ('PUS', '김해공항', '김해국제공항', '부산')
    CJU = ('CJU', '제주공항', '제주국제공항', '제주')
    USN = ('USN', '울산공항', '울산공항', '울산')
    KWJ = ('KWJ', '광주공항', '광주공항', '광주')
    RSU = ('RSU', '여수공항', '여수공항', '여수')
    TAE = ('TAE', '대구공항', '대구국제공항', '대구')
    YNY = ('YNY', '양양공항', '양양국제공항', '양양')
    MWX = ('MWX', '무안공항', '무안국제공항', '무안')
    CJJ = ('CJJ', '청주공항', '청주국제공항', '청주')
    KUV = ('KUV', '군산공항', '군산공항', '군산')
    WJU = ('WJU', '원주공항', '원주공항', '원주')
    KPO = ('KPO', '포항공항', '포항경주공항', '포항')

    def __init__(self, code, simple_name, full_name, location):
        self.code = code
        self.simple_name = simple_name
        self.full_name = full_name
        self.location = location


class Airlines(Enum):
    AAR = ('AAR', '아시아나항공', 'https://m.flyasiana.com', 'https://flyasiana.com')
    ABL = ('ABL', '에어부산', 'https://m.airbusan.com', 'https://airbusan.com')
    ASV = ('ASV', '에어서울', 'https://m.flyairseoul.com', 'https://flyairseoul.com')
    EOK = ('EOK', '에어로케이', 'https://www.aerok.com/kr', 'https://www.aerok.com/kr')
    FGW = ('FGW', '플라이강원', 'https://m.flygangwon.com', 'https://flygangwon.com/')
    JJA = ('JJA', '제주항공', 'https://www.jejuair.net', 'https://www.jejuair.net')
    JNA = ('JNA', '진에어', 'https://www.jinair.com/booking/index', 'https://www.jinair.com/booking/index')
    KAL = ('KAL', '대한항공', 'https://www.koreanair.com/kr/ko', 'https://www.koreanair.com/kr/ko')
    TWB = ('TWB', '티웨이항공', 'https://m.twayair.com', 'https://www.twayair.com')

    def __init__(self, code, kor_name, mo_page, pc_page):
        self.code = code
        self.kor_name = kor_name
        self.mo_page = mo_page
        self.pc_page = pc_page

