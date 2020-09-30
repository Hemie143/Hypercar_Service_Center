from django.views import View
from django.http.response import HttpResponse


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        html = '<h2>Welcome to the Hypercar Service!</h2>'
        return HttpResponse(html)
