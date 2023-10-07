from django.shortcuts import redirect


class RedirectIfAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path in ['/registration/login/']:
                return redirect('index')  # Replace 'index' with the URL name of your index page
        return self.get_response(request)
