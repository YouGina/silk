class XForwardedForMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            request.META["REMOTE_ADDR"] = xff.split(",")[0].strip()
        return self.get_response(request)
