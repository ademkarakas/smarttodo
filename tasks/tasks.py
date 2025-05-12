from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task
import logging
import traceback

logger = logging.getLogger(__name__)


@shared_task
def check_and_send_reminders():
    # Aktuelle Zeit in lokale Zeitzone umwandeln
    now = timezone.localtime()

    # Aufgaben finden, die eine Erinnerung benötigen
    tasks = Task.objects.filter(
        # Erinnerungszeit mit lokaler Zeit vergleichen
        reminder_time__lte=now,
        reminder_sent=False,
        is_completed=False
    )

    for task in tasks:
        try:
            # Wenn Aufgabe einen Benutzer hat, sende eine E-Mail
            if task.user and task.user.email:
                # Erinnerungszeit in lokale Zeitzone umwandeln
                local_reminder_time = timezone.localtime(task.reminder_time)

                send_mail(
                    subject='🕒 Erinnerung: Aufgabe wartet',
                    message=f'Ihre Aufgabe „{task.title}" wartet auf Erledigung. Ursprüngliche Erinnerungszeit: {local_reminder_time.strftime("%d.%m.%Y %H:%M")}',
                    from_email='noreply@todo.com',
                    recipient_list=[task.user.email],
                    fail_silently=False  # Fehler für Debugging nicht unterdrücken
                )

            task.send_notification()
            task.reminder_sent = True
            task.save()
            logger.info(f"Erinnerung gesendet für Aufgabe {task.id}")
        except Exception as e:
            logger.error(f"Fehler bei Aufgabe {task.id}: {e}")
            logger.error(traceback.format_exc())  # Vollständige Fehler-Rückverfolgung loggen


@shared_task
def sende_aufgaben_erinnerungen():
    """
    Diese Aufgabe sendet Erinnerungen für Aufgaben,
    die in den nächsten 10 Minuten fällig werden.
    """
    # Aktuelle Zeit in lokale Zeitzone umwandeln
    now = timezone.localtime()

    # Aufgaben finden, die in den nächsten 10 Minuten fällig werden
    naechste_aufgaben = Task.objects.filter(
        is_completed=False,
        # Zeitvergleiche in lokaler Zeitzone durchführen
        due_date__lte=now + timedelta(minutes=10),
        due_date__gte=now
    )

    for aufgabe in naechste_aufgaben:
        try:
            # Fälligkeitsdatum in lokale Zeitzone umwandeln
            local_due_date = timezone.localtime(aufgabe.due_date)

            # Benutzer-spezifische E-Mail senden
            if aufgabe.user and aufgabe.user.email:
                send_mail(
                    subject='🕒 Erinnerung: Fällige Aufgabe',
                    message=f'Ihre Aufgabe „{aufgabe.title}" ist bald fällig (bis {local_due_date.strftime("%d.%m.%Y %H:%M")}).',
                    from_email='noreply@todo.com',
                    recipient_list=[aufgabe.user.email],
                    fail_silently=False  # Fehler für Debugging nicht unterdrücken
                )

                logger.info(f"Erinnerungsmail gesendet für Aufgabe {aufgabe.id}")
        except Exception as e:
            logger.error(f"Fehler bei Aufgabe {aufgabe.id}: {e}")
            logger.error(traceback.format_exc())  # Vollständige Fehler-Rückverfolgung loggen


# Zusatzfunktion zur Überprüfung der Zeitzoneneinstellungen
def log_time_info():
    """
    Hilfsfunktion zum Überprüfen der Zeitzoneneinstellungen
    """
    logger.info(f"Aktuelle UTC-Zeit: {timezone.now()}")
    logger.info(f"Aktuelle lokale Zeit: {timezone.localtime()}")
    logger.info(f"Systemzeitzone: {timezone.get_current_timezone_name()}")