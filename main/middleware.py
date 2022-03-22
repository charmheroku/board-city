from user_agents import parse


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        ua_string = request.META["HTTP_USER_AGENT"]
        user_agent = parse(ua_string)
        if user_agent.is_mobile:
            request.is_mobile = True
        else:
            request.is_mobile = False
