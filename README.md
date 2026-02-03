# SmartTodo - Intelligente Aufgabenverwaltung

Eine moderne, benutzerfreundliche Aufgabenverwaltungsanwendung, die mit Django entwickelt wurde. SmartTodo hilft Ihnen, Ihre Aufgaben effizient zu organisieren, zu priorisieren und termingerecht zu erledigen.

## ✨ Features

### Kernfunktionalität
- **Aufgabenverwaltung**: Erstellen, Bearbeiten, Löschen und Verwalten von Aufgaben
- **Intelligente Kategorisierung**: Organisieren Sie Aufgaben in Kategorien wie Arbeit, Haushalt, Gesundheit, Einkaufen, Finanzen, Bildung, Sport, Freizeit und Familie
- **Prioritätssystem**: Drei Prioritätsstufen (Niedrig, Mittel, Hoch) für bessere Aufgabenorganisation
- **Fälligkeitsdaten**: Setzen Sie Deadlines und verfolgen Sie überfällige Aufgaben
- **Erinnerungen**: Automatische E-Mail-Benachrichtigungen für anstehende Aufgaben

### Benutzerfreundlichkeit
- **Responsive Design**: Optimiert für Desktop, Tablet und mobile Geräte
- **Benutzerauthentifizierung**: Sichere Registrierung und Anmeldung
- **Persönliche Aufgabenlisten**: Jeder Benutzer verwaltet seine eigenen Aufgaben
- **Filteroptionen**: Filtern nach Priorität, Status und Fälligkeitsdatum
- **Smart Task Input**: Intelligente Eingabe mit Natural Language Processing (dateparser)

### Erweiterte Funktionen
- **E-Mail-Benachrichtigungen**: Automatische Erinnerungen für fällige Aufgaben
- **Benutzerprofile**: Erweiterte Benutzerprofile mit Kontaktinformationen
- **Kontaktformular**: Integriertes Kontaktformular für Benutzeranfragen
- **Datenschutz**: Impressum, Nutzungsbedingungen und Datenschutzerklärung
- **PWA-Unterstützung**: Progressive Web App Funktionalität

## 🚀 Technologie-Stack

- **Backend Framework**: Django 5.2.1
- **Datenbank**: 
  - SQLite (Entwicklung)
  - PostgreSQL (Produktion, via psycopg2-binary)
- **Task Queue**: Celery 5.5.2 mit Redis
- **Webserver**: Gunicorn 23.0.0
- **Static Files**: WhiteNoise 6.9.0
- **Natural Language Processing**: dateparser 1.2.1
- **Authentication**: Django Built-in Auth + PyJWT 2.9.0
- **Frontend**: HTML, CSS, JavaScript (mit Service Worker für PWA)

## 📋 Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)
- Redis Server (für Celery-Task-Queue)
- PostgreSQL (für Produktion, optional für Entwicklung)

## 🛠️ Installation

### 1. Repository klonen

```bash
git clone https://github.com/ademkarakas/smarttodo.git
cd smarttodo
```

### 2. Virtuelle Umgebung erstellen und aktivieren

```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Umgebungsvariablen konfigurieren

Erstellen Sie eine `.env` Datei im Projektverzeichnis:

```env
SECRET_KEY=ihr-geheimer-schlüssel-hier
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # Für Entwicklung

# E-Mail Konfiguration (optional)
EMAIL_HOST_USER=ihre-email@gmail.com
EMAIL_HOST_PASSWORD=ihr-app-passwort

# Für Produktion auf Render
RENDER_EXTERNAL_HOSTNAME=ihre-app.onrender.com
```

### 5. Datenbank migrieren

```bash
python manage.py migrate
```

### 6. Superuser erstellen (optional)

```bash
python manage.py createsuperuser
```

### 7. Static Files sammeln

```bash
python manage.py collectstatic --no-input
```

### 8. Entwicklungsserver starten

```bash
python manage.py runserver
```

Die Anwendung ist nun unter `http://127.0.0.1:8000/` erreichbar.

## 🔧 Konfiguration

### Redis für Celery (optional)

Für Erinnerungsfunktionen benötigen Sie Redis:

```bash
# Redis installieren (Ubuntu/Debian)
sudo apt-get install redis-server

# Redis starten
redis-server
```

Celery Worker starten:

```bash
celery -A smarttodo worker -l info
```

### E-Mail Konfiguration

Für E-Mail-Benachrichtigungen konfigurieren Sie die folgenden Einstellungen in `settings.py`:

- `EMAIL_HOST_USER`: Ihre E-Mail-Adresse
- `EMAIL_HOST_PASSWORD`: Ihr App-Passwort (für Gmail verwenden Sie ein App-Passwort)

## 📱 Verwendung

### Registrierung und Anmeldung

1. Besuchen Sie die Startseite
2. Klicken Sie auf "Registrieren"
3. Füllen Sie das Registrierungsformular aus
4. Melden Sie sich mit Ihren Zugangsdaten an

### Aufgaben verwalten

1. **Neue Aufgabe erstellen**: Klicken Sie auf "Neue Aufgabe" und füllen Sie das Formular aus
2. **Aufgabe bearbeiten**: Klicken Sie auf das Bearbeiten-Symbol bei einer Aufgabe
3. **Aufgabe als erledigt markieren**: Klicken Sie auf das Häkchen-Symbol
4. **Aufgabe löschen**: Klicken Sie auf das Löschen-Symbol
5. **Filtern**: Verwenden Sie die Filteroptionen, um Aufgaben nach Priorität oder Status zu sortieren

### Erinnerungen einrichten

Beim Erstellen oder Bearbeiten einer Aufgabe können Sie:
- Ein Fälligkeitsdatum festlegen
- Eine Erinnerungszeit einstellen
- Die Priorität und Kategorie auswählen

Das System sendet automatisch E-Mail-Benachrichtigungen, wenn Erinnerungen fällig werden.

## 🚢 Deployment

### Deployment auf Render

Die Anwendung ist für das Deployment auf Render vorbereitet:

1. Verbinden Sie Ihr GitHub-Repository mit Render
2. Die `build.sh` Datei wird automatisch für den Build-Prozess verwendet
3. Konfigurieren Sie die Umgebungsvariablen in Render:
   - `SECRET_KEY`
   - `DATABASE_URL` (PostgreSQL)
   - `EMAIL_HOST_USER`
   - `EMAIL_HOST_PASSWORD`
   - `RENDER_EXTERNAL_HOSTNAME`

### Manuelles Deployment

```bash
# Build-Skript ausführen
./build.sh
```

Das Skript führt folgende Schritte aus:
1. Pip-Upgrade
2. Installation der Abhängigkeiten
3. Sammeln der Static Files
4. Datenbankmigrationen

## 📁 Projektstruktur

```
smarttodo/
├── smarttodo/              # Hauptprojektverzeichnis
│   ├── settings.py        # Django-Einstellungen
│   ├── urls.py            # URL-Konfiguration
│   ├── wsgi.py            # WSGI-Konfiguration
│   └── celery.py          # Celery-Konfiguration
├── tasks/                  # Hauptanwendung
│   ├── models.py          # Datenmodelle (Task, Profile, ContactMessage)
│   ├── views.py           # View-Funktionen
│   ├── forms.py           # Formulare
│   ├── tasks.py           # Celery-Tasks
│   ├── templates/         # HTML-Templates
│   └── static/            # Statische Dateien (CSS, JS)
├── templates/              # Projektweite Templates
├── static/                 # Projektweite statische Dateien
├── staticfiles/            # Gesammelte statische Dateien
├── manage.py              # Django-Management-Skript
├── requirements.txt       # Python-Abhängigkeiten
├── build.sh               # Build-Skript für Deployment
└── README.md              # Diese Datei
```

## 🔒 Sicherheit

Die Anwendung implementiert verschiedene Sicherheitsmaßnahmen:

- **Authentifizierung**: Django's eingebautes Authentifizierungssystem
- **CSRF-Protection**: Cross-Site Request Forgery Protection aktiviert
- **Password Hashing**: Sichere Passwort-Hashing-Algorithmen
- **User Isolation**: Benutzer können nur ihre eigenen Aufgaben sehen und bearbeiten
- **HTTPS Ready**: Vorbereitet für HTTPS-Deployment

## 🌐 Mehrsprachigkeit

Die Anwendung unterstützt:
- Deutsch (Standardsprache)
- Englisch

Zeitzone: Europe/Berlin

## 🤝 Beitragen

Beiträge sind willkommen! Bitte befolgen Sie diese Schritte:

1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Pushen Sie zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## 👤 Autor

**Adem Karakas**

- GitHub: [@ademkarakas](https://github.com/ademkarakas)
- E-Mail: antonmeierentwickler@gmail.com

## 🙏 Danksagungen

- Django Framework und Community
- Alle Contributors, die an diesem Projekt mitgewirkt haben
- Open-Source-Bibliotheken, die dieses Projekt möglich gemacht haben

## 📞 Support

Bei Fragen oder Problemen:
- Öffnen Sie ein Issue auf GitHub
- Kontaktieren Sie uns über das Kontaktformular in der Anwendung
- E-Mail: antonmeierentwickler@gmail.com

## 🔄 Versionshistorie

### Version 1.0.0
- Erste öffentliche Version
- Grundlegende Aufgabenverwaltung
- Benutzerauthentifizierung
- E-Mail-Benachrichtigungen
- Responsive Design
- PWA-Unterstützung

---

**Live-Demo**: [smarttodo-210h.onrender.com](https://smarttodo-210h.onrender.com)

**Hinweis**: Dieses Projekt wird aktiv weiterentwickelt. Weitere Features sind in Planung!
