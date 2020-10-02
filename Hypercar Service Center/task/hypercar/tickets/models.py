from django.db import models


class Ticket(models.Model):
    TASKS = [
        ('OIL', 'change_oil'),
        ('TIR', 'inflate_tires'),
        ('DIA', 'diagnostic'),
    ]

    ticket_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=3,
                            choices=TASKS)
    open_status = models.BooleanField(default=True)
