from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

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
        max_id = 0
        high_ticket = Ticket.objects.all().order_by('-ticket_id')
        if high_ticket:
            max_id = high_ticket[0].ticket_id

        open_tickets = Ticket.objects.filter(open_status='OP')
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

        new_ticket = Ticket.objects.create(ticket_id=max_id + 1,
                                           type=type,
                                           open_status='OP',
                                           )
        new_id = new_ticket.ticket_id
        context = {'ticket_id': new_id, 'wait_time': wait_time}
        return render(request, 'tickets/ticket.html', context=context)

class OperatorView(View):
    def get(self, request, *args, **kwargs):
        open_tickets = Ticket.objects.filter(open_status='OP')
        open_oil = open_tickets.filter(type='OIL').count()
        open_tires = open_tickets.filter(type='TIR').count()
        open_diag = open_tickets.filter(type='DIA').count()
        context = {'open_oil': open_oil,
                   'open_tires': open_tires,
                   'open_diag': open_diag,
                   }
        return render(request, 'tickets/operator.html', context=context)

    def post(self, request, *args, **kwargs):
        open_tickets = Ticket.objects.filter(open_status='OP')
        open_oil = open_tickets.filter(type='OIL')
        if open_oil:
            id = open_oil.order_by('ticket_id')[0].ticket_id
        else:
            open_tires = open_tickets.filter(type='TIR')
            if open_tires:
                id = open_tires.order_by('ticket_id')[0].ticket_id
            else:
                open_diag = open_tickets.filter(type='DIA')
                if open_diag:
                    id = open_diag.order_by('ticket_id')[0].ticket_id
                else:
                    id = 0
        if id:
            busy_ticket = Ticket.objects.filter(open_status='BU')
            if busy_ticket:
                busy_ticket.first().open_status = 'CL'
                busy_ticket.first().save()
            next_ticket = Ticket.objects.get(ticket_id=id)
            next_ticket.open_status = 'BU'
            next_ticket.save()

        return render(request, 'tickets/next.html', context={'id': id})

class NextView(View):
    def get(self, request, *args, **kwargs):
        busy_ticket = Ticket.objects.filter(open_status='BU')
        if busy_ticket:
            id = busy_ticket.first().ticket_id
        else:
            id = 0
        return render(request, 'tickets/next.html', context={'id': id})
