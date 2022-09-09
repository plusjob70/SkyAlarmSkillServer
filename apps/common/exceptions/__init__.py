class NotExistContext(Exception):
    def __str__(self):
        return 'Context is not exist.'


class ExceededAlarmCountLimit(Exception):
    def __str__(self):
        return 'The number of alarms that can be registered has been exceeded.'


class NotExistObjectId(Exception):
    def __str__(self):
        return 'The corresponding ID does not exist.'


class NotReadyYet(Exception):
    def __str__(self):
        return 'It is not ready yet'
