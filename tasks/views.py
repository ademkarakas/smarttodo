import traceback

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, logger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, ContactMessage
from .forms import TaskForm, SmartTaskForm, TaskEditForm,RegisterForm
import dateparser
from django.utils.timezone import now
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def home_view(request):
    if request.user.is_authenticated:
        return redirect('alle_aufgaben')

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            print(f"Empfangene Daten: Name={name}, Email={email}, Subject={subject}")  # Debug-Info

            # E-Mail senden
            send_mail(
                subject=f'Neue Kontaktanfrage: {subject}',
                message=f'Name: {name}\nE-Mail: {email}\nNachricht: {message}',
                from_email=settings.DEFAULT_FROM_EMAIL,  # Änderung hier
                recipient_list=['antonmeierentwickler@gmail.com'],
                fail_silently=False,
            )
            # Nachricht in der Datenbank speichern
            contact_message = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            contact_message.save()

            messages.success(request, 'Ihre Nachricht wurde erfolgreich gesendet!')
            return redirect('home')
        except Exception as e:
            print(f"Fehler beim E-Mail-Versand: {str(e)}")  # Debug-Info
            messages.error(request, 'Beim Senden der Nachricht ist ein Fehler aufgetreten.')

    return render(request, 'tasks/home.html')

def nutzungsbedingungen(request):
    return render(request,'tasks/nutzungsbedingungen.html')

def datenschutz(request):
    return render(request,'tasks/datenschutz.html')


def impressum(request):
    return render(request, 'tasks/impressum.html')

def privacy_policy(request):
    context = {
        'current_date': datetime.now()
    }
    return render(request, 'datenschutz.html', context)

def cookie_settings(request):
    if request.method == 'POST':
        # Handle cookie preferences saving
        pass
    return render(request, 'tasks/cookie_settings.html')

@login_required
def task_list(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user

            # Kombiniere Datum und Uhrzeit
            due_datetime_str = request.POST.get('due_datetime')
            if due_datetime_str:
                try:
                    task.due_date = timezone.make_aware(datetime.strptime(due_datetime_str, '%Y-%m-%dT%H:%M'))
                except ValueError:
                    pass

            reminder_time_str = request.POST.get('reminder_time')
            if reminder_time_str:
                try:
                    task.reminder_time = timezone.make_aware(datetime.strptime(reminder_time_str, '%Y-%m-%dT%H:%M'))
                except ValueError:
                    pass

            task.save()
            messages.success(request, 'Aufgabe erfolgreich erstellt!')
            return redirect('task_list')
    else:
            form = TaskForm()

    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'tasks/task_list.html', {
            'tasks': tasks,
            'form': form
        })


@login_required
def smart_task_create(request):
    if request.method == 'POST':
        form = SmartTaskForm(request.POST)
        if form.is_valid():
            # Bei SmartTaskForm müssen wir manuell ein Task-Objekt erstellen
            raw_input = form.cleaned_data['raw_input']
            priority = form.cleaned_data['priority']
            category = form.cleaned_data['category']

            # Versuchen, ein Datum aus dem Text zu extrahieren
            parsed_date = dateparser.parse(raw_input, settings={'STRICT_PARSING': False})

            # Neue Aufgabe erstellen
            task = Task(
                user=request.user,
                title=raw_input,  # Als Titel den Rohtext verwenden
                priority=priority,
                category=category,
                due_date=parsed_date
            )
            task.save()
            messages.success(request, 'Aufgabe erfolgreich erstellt!')
            return redirect('task_list')
    else:
        form = SmartTaskForm()

    return render(request, 'tasks/smart_task_create.html', {'form': form})


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aufgabe erfolgreich aktualisiert!')
            return redirect('alle_aufgaben')
    else:
        form = TaskEditForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

@login_required
def reactivate_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = False
    task.save()
    messages.success(request, 'Aufgabe wurde reaktiviert!')
    return redirect('alle_aufgaben')

@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = True
    task.save()
    messages.success(request, 'Aufgabe als erledigt markiert!')
    return redirect('alle_aufgaben')


@login_required
def alle_aufgaben(request):
    # Alle Aufgaben des aktuellen Benutzers finden
    tasks = Task.objects.filter(user=request.user)

    # Erweiterte Filterlogik
    priority_filter = request.GET.get('priority')
    status_filter = request.GET.get('status')

    # Prioritätsfilter
    if priority_filter == 'hoch':
        tasks = tasks.filter(priority='high')
    elif priority_filter == 'mittel':
        tasks = tasks.filter(priority='medium')
    elif priority_filter == 'niedrig':
        tasks = tasks.filter(priority='low')
    elif priority_filter == 'heute':
        today = now().date()
        tasks = tasks.filter(due_date__date=today)

    # Statusfilter
    if status_filter == 'offen':
        tasks = tasks.filter(is_completed=False)
    elif status_filter == 'erledigt':
        tasks = tasks.filter(is_completed=True)

    # Standard-Sortierung
    tasks = tasks.order_by('-created_at')

    return render(request, 'tasks/all_tasks.html', {
        'tasks': tasks,
        'active_priority': priority_filter,
        'active_status': status_filter
    })


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    messages.success(request, 'Aufgabe erfolgreich gelöscht!')
    return redirect('alle_aufgaben')


from .forms import RegisterForm  # Statt UserCreationForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto für {username} wurde erstellt! Sie können sich jetzt einloggen.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})


@login_required
def add_suggestion(request):
    if request.method == 'POST':
        suggested_task = request.POST.get('suggested_task')
        if suggested_task:
            task = Task(
                user=request.user,
                title=suggested_task,
                priority='medium',
                category='Sonstiges'
            )
            task.save()
            messages.success(request, 'Vorgeschlagene Aufgabe hinzugefügt!')
    return redirect('task_list')


@login_required
def check_reminders(request):
    try:
        # Aktuelle Zeit in lokale Zeitzone umwandeln
        jetzt = timezone.localtime()

        tasks = Task.objects.filter(
            user=request.user,
            # Erinnerungszeit mit lokaler Zeit vergleichen
            reminder_time__lte=jetzt,
            reminder_sent=False,
            is_completed=False
        ).select_related('user')

        tasks_data = []
        for task in tasks:
            # Erinnerungszeit in lokale Zeitzone umwandeln
            local_reminder_time = timezone.localtime(task.reminder_time)

            # Fälligkeitsdatum in lokale Zeitzone umwandeln
            local_due_date = timezone.localtime(task.due_date) if task.due_date else None

            tasks_data.append({
                'id': task.id,
                'title': task.title,
                # Lokalisierte Zeitformatierung
                'due_date': local_due_date.strftime("%d.%m.%Y %H:%M") if local_due_date else None,
                # Zusätzliche Debugging-Informationen
                'original_reminder_time': task.reminder_time,
                'localized_reminder_time': local_reminder_time
            })

            # Als gesendet markieren
            task.reminder_sent = True
            task.save()

        # Zusätzliche Logging-Informationen
        logger.info(f"Aktuelle lokale Zeit: {jetzt}")
        logger.info(f"Gefundene Tasks: {len(tasks_data)}")

        return JsonResponse({
            'tasks': tasks_data,
            # Aktuelle lokale Zeit in der Antwort hinzufügen
            'current_local_time': jetzt.strftime("%d.%m.%Y %H:%M %Z")
        })
    except Exception as e:
        # Detaillierte Fehler-Logging
        logger.error(f"Fehler in check_reminders: {str(e)}")
        logger.error(f"Vollständige Fehlermeldung: {traceback.format_exc()}")

        return JsonResponse({'error': 'Ein Fehler ist aufgetreten'}, status=500)