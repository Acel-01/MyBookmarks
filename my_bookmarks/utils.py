from rest_framework.views import exception_handler

# A Custom exception handler that moves the exception 'detail' to a 'message' key in the dictionary
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if not isinstance(response.data, list):
            if response.data.get('detail'):
                response.data['message'] = response.data.pop('detail')


    return response
