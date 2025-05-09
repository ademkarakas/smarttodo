"""
URL configuration for smarttodo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from tasks import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Neue Startseite (Landing Page)
    path('', views.home_view, name='home'),
    path('nutzungsbedingungen',views.nutzungsbedingungen,name='nutzungsbedingungen'),
    path('datenschutz',views.datenschutz, name='datenschutz'),
    path('impressum/', views.impressum, name='impressum'),
    path('cookie-einstellungen/', views.cookie_settings, name='cookie_settings'),
    path('datenschutz/', views.privacy_policy, name='privacy_policy'),

    # Aufgabenliste (für eingeloggte User)
    path('aufgaben/', views.task_list, name='task_list'),
    path('alle/', views.alle_aufgaben, name='alle_aufgaben'),

    # Aufgabenaktionen
    path('complete/<int:pk>/', views.complete_task, name='complete_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('add-suggestion/', views.add_suggestion, name='add_suggestion'),
    path('task/<int:pk>/edit/', views.edit_task, name='edit_task'),

    # Authentifizierung
    path('login/', LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='tasks/logout.html'
    ), name='logout'),
    path('register/', views.register, name='register'),

    # Erinnerung
    path('check_reminders/', views.check_reminders, name='check_reminders'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/password_reset/done/'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('contact/', views.home_view, name='contact'),

    path('task/<int:pk>/reactivate/', views.reactivate_task, name='reactivate_task'),

]




