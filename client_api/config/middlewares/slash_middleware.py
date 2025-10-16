class SlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            if not request.path.endswith('/'):
                request.path_info += '/'
                response = self.get_response(request)
            else:
                request.path_info = request.path_info.rstrip('/')
                response = self.get_response(request)

        return response
