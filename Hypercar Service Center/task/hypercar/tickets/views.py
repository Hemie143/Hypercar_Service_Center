from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render

from tickets.models import Ticket


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        html = '<h2>Welcome to the Hypercar Service!</h2>'
        return HttpResponse(html)


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')


class TicketView(View):
    def get(self, request, task, *args, **kwargs):
        '''
        max_id = Ticket.objects.order_by('-ticket_id')
        if not max_id:
            max_id = 0
        else:
            print('somethin')
            print(max_id)
            max_id = max_id[0].ticket_id
        print(f'max_id: {max_id}')
        '''

        open_tickets = Ticket.objects.filter(open_status=True)
        open_oil = open_tickets.filter(type='OIL').count()
        open_tires = open_tickets.filter(type='TIR').count()
        open_diag = open_tickets.filter(type='DIA').count()

        if task == 'change_oil':
            wait_time = open_oil * 2
            type = 'OIL'
        elif task == 'inflate_tires':
            wait_time = open_oil * 2 + open_tires * 5
            type = 'TIR'
        elif task == 'diagnostic':
            wait_time = open_oil * 2 + open_tires * 5 + open_diag * 30
            type = 'DIA'

        new_ticket = Ticket.objects.create(type=type,
                                           open_status=True,
                                           )
        new_id = new_ticket.ticket_id
        context = {'ticket_id': new_id, 'wait_time': wait_time}
        return render(request, 'tickets/ticket.html', context=context)