from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        html = '<h2>Welcome to the Hypercar Service!</h2>'
        return HttpResponse(html)


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/ticket.html')