from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.template.defaulttags import now
from django.utils import timezone
from .models import Task
import logging

logger = logging.getLogger(__name__)


@shared_task
def check_and_send_reminders():
    now = timezone.now()
    tasks = Task.objects.filter(
        reminder_time__lte=now,
        reminder_sent=False,
        is_completed=False
    )

    for task in tasks:
        try:
            task.send_notification()
            task.reminder_sent = True
            task.save()
            logger.info(f"Erinnerung gesendet für Aufgabe {task.id}")
        except Exception as e:
            logger.error(f"Fehler bei Aufgabe {task.id}: {e}")

@shared_task
def sende_aufgaben_erinnerungen():
    """
    Diese Aufgabe prüft alle noch nicht erledigten Aufgaben,
    die innerhalb der nächsten 10 Minuten fällig sind,
    und sendet eine Erinnerungs-E-Mail.
    """

    # Alle offenen Aufgaben mit Fälligkeit in den nächsten 10 Minuten
    naechste_aufgaben = Task.objects.filter(
        is_completed=False,
        due_date__lte=now() + timedelta(minutes=10),
        due_date__gte=now()  # (optional) Nur zukünftige Aufgaben
    )

    for aufgabe in naechste_aufgaben:
        send_mail(
            subject='🕒 Erinnerung: Fällige Aufgabe',
            message=f'Ihre Aufgabe „{aufgabe.title}“ ist bald fällig (bis {aufgabe.due_date.strftime("%d.%m.%Y %H:%M")}).',
            from_email='noreply@todo.com',
            recipient_list=['nutzer@email.com'],  # Optional: dynamisch je Benutzer
            fail_silently=True  # Fehler beim Senden unterdrücken
        )
