from mongoengine import *


class Route(Document):
    departure = StringField(required=True)
    destination = StringField(required=True)

    meta = {
        'allow_inheritance': True
    }


class Alarm(Route):
    register_datetime = DateTimeField(required=True)
    user_id = StringField(required=True)
    user_type = StringField(required=True)
    user_timezone = StringField(required=True)
    departure_date = DateField(required=True)
    age = StringField(required=True, default='adult')



class Ticket(Route):
    flight_id = StringField(default='None')
    airline = StringField(required=True)
    departure_datetime = DateTimeField(required=True)
    arrival_datetime = DateTimeField(required=True)
    seat_class = StringField(required=True, default='CLASS-1')
    adult_fees = IntField(required=True)
    child_fees = IntField(required=True)
    search_datetime = DateTimeField(required=True)

