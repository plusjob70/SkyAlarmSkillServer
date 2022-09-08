from typing import Union
from functools import partial
from flask import make_response, jsonify, Response


class ChatbotParamValidResponse:
    @staticmethod
    def response(status: str, value: Union[int, str] = None, data: dict = None) -> Response:
        params = {'status': status}

        if value is not None:
            params['value'] = value

        if data is not None:
            params['data'] = data

        return make_response(jsonify(params))

    ok = partial(response, 'SUCCESS')
    fail = partial(response, 'FAIL')
    error = partial(response, 'ERROR')


class ChatbotSkillResponse:
    @staticmethod
    def response(version: str = '2.0', template: dict = None, context: dict = None, data: dict = None) -> Response:
        params = {'version': version}

        if template is not None:
            params['template'] = template

        if context is not None:
            params['context'] = context

        if data is not None:
            params['data'] = data

        return make_response(jsonify(params))


class ChatbotResponseCode:
    SUCCESS_INSERT = 1010
    SUCCESS_DELETE = 1020

    NOT_EXIST_ARGUMENT_ERROR = 6001
    NOT_EXIST_CONTEXT_ERROR = 6002

    EXCEEDED_REGISTER_LIMIT = 6011

    ALREADY_DELETED_ERROR = 6021

