from celery import Task
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Task,ContactMessage

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    reminder_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        help_text="Wann möchten Sie erinnert werden?"
    )

    class Meta:
        model = Task
        fields = ['title', 'priority', 'category', 'due_date', 'is_completed']  # is_completed hinzufügen
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Widget für Checkbox
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Entferne das due_date Feld, da wir es manuell behandeln
            if 'due_date' in self.fields:
                del self.fields['due_date']

class SmartTaskForm(forms.Form):
    raw_input = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'z. B. „Treffen morgen um 10 Uhr“'})
    )
    priority = forms.ChoiceField(
        choices=Task.PRIORITAETEN,  # Verwende die Prioritätsoptionen aus dem Modell
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='medium',  # Standardwert
        label='Priorität'
    )
    category = forms.ChoiceField(
        choices=Task.CATEGORY_CHOICES,  # Verwende die Kategorieoptionen aus dem Modell
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='Sonstiges',  # Standardwert
        label='Kategorie'
    )

class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'category', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefon = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefon', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.telefon = self.cleaned_data['telefon']
            profile.save()

        return user


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
