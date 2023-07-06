from rest_framework import renderers
import json

from json import JSONEncoder
from uuid import UUID

old_default = JSONEncoder.default

def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    return old_default(self, obj)

JSONEncoder.default = new_default

class APIRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data_ = data
        if 'ErrorDetail' in str(data_):
            message = "The data you entered is not valid"

            if not isinstance(data, list):
                if not data_.get("message"):
                    message = "The data you entered is not valid"
                else:
                    message = data_.pop("message")

            dict_ = {
                'message': message,
                'status': False,
                'errors': data_,
            }

            if not data_:
                dict_.pop("errors")

            response = json.dumps(dict_)
        else:
            if data_:
                if data_.get("message"):
                    message = data_.pop('message')
                else:
                    message = "Request is Successful"

                if 'data_body_' in str(data_):
                    data_ = data_.pop('data_body_')

                if "count" in data_:
                    message = data_["results"][0].pop("message")[0]

                response = json.dumps(
                    {
                        'message': message,
                        'status': True,
                        'data': data_,
                    }
                )
            else:
                response = b''

        return response
