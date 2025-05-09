from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# Modell für Aufgaben
class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    is_completed = models.BooleanField(default=False, verbose_name="Erledigt")

    PRIORITAETEN = [
        ('low', 'Niedrig'),
        ('medium', 'Mittel'),
        ('high', 'Hoch'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITAETEN, default='medium', verbose_name='Priorität')

    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Fälligkeitsdatum")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    CATEGORY_CHOICES = [
        ('Arbeit', 'Arbeit'),
        ('Haushalt', 'Haushalt'),
        ('Gesundheit', 'Gesundheit'),
        ('Sonstiges', 'Sonstiges'),
        ('Einkaufen', 'Einkaufen'),
        ('Finanzen', 'Finanzen'),
        ('Bildung', 'Bildung'),
        ('Sport', 'Sport'),
        ('Freizeit', 'Freizeit'),
        ('Familie', 'Familie'),

    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Sonstiges', verbose_name='Kategorie')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Benutzer")
    reminder_time = models.DateTimeField(null=True, blank=True, verbose_name="Erinnerungszeit")

    reminder_sent = models.BooleanField(default=False, verbose_name="Erinnerung gesendet")
    notification_sent = models.BooleanField(default=False, verbose_name="Benachrichtigung gesendet")

    # Überprüfung, ob die Erinnerung fällig ist
    def is_reminder_due(self):
        return self.reminder_time and timezone.now() >= self.reminder_time

    @property
    def is_overdue(self):
        return self.due_date and timezone.now() > self.due_date

    # Benachrichtigung senden (Browser & Mail)
    def send_notification(self):
        self.send_browser_notification()
        if self.user.email:
            self.send_email_notification()
        self.notification_sent = True
        self.save()

    # Diese Funktion muss im Frontend über JavaScript umgesetzt werden
    def send_browser_notification(self):
        pass  # Client-seitige Browser-Notifikation

    # Senden einer Erinnerungs-E-Mail
    def send_email_notification(self):
        if self.user.email:
            subject = f"Erinnerung: {self.title}"
            message = f"""
            Hallo {self.user.username},

            Sie haben eine Aufgabe, die demnächst fällig ist:

            Titel: {self.title}
            Priorität: {self.get_priority_display()}
            Fällig am: {self.due_date.strftime('%d.%m.%Y %H:%M')}

            Viele Grüße,
            Ihr Aufgabenplaner
            """
            send_mail(
                subject,
                message.strip(),
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                fail_silently=False,
            )

    def __str__(self):
        return self.title


# Benutzerprofil (optional mit Telefonnummer)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profil"


# Automatische Profilerstellung beim Erstellen eines Benutzers


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="E-Mail")
    subject = models.CharField(max_length=200, verbose_name="Betreff")
    message = models.TextField(verbose_name="Nachricht")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gesendet am")

    class Meta:
        verbose_name = "Kontaktnachricht"
        verbose_name_plural = "Kontaktnachrichten"

    def __str__(self):
        return f"{self.subject} von {self.name}"
