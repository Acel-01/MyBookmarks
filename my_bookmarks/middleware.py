from django.core.cache import cache
from rest_framework.settings import api_settings


class RateLimitResponseHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        THROTTLE_RATES = api_settings.DEFAULT_THROTTLE_RATES

        response = self.get_response(request)

        if request.user.is_authenticated:
            rate = THROTTLE_RATES["user"]
            num_requests, period = rate.split('/')
            response['x-ratelimit-limit'] = num_requests

            user_pk = request.user.pk

            # User is authenticated, apply rate limit based on user PK
            cache_key = f'throttle_user_{user_pk}'
        else:
            rate = THROTTLE_RATES["anon"]
            num_requests, period = rate.split('/')
            response['x-ratelimit-limit'] = num_requests

            xff = request.META.get('HTTP_X_FORWARDED_FOR')
            remote_addr = request.META.get('REMOTE_ADDR')
            num_proxies = api_settings.NUM_PROXIES

            if num_proxies is not None:
                if num_proxies == 0 or xff is None:
                    return remote_addr
                addrs = xff.split(',')
                client_addr = addrs[-min(num_proxies, len(addrs))]
                return client_addr.strip()

            ident = ''.join(xff.split()) if xff else remote_addr

            cache_key = f'throttle_anon_{ident}'

        history = cache.get(cache_key, [])

        response['x-ratelimit-remaining'] = int(num_requests) - int(len(history))

        return response
