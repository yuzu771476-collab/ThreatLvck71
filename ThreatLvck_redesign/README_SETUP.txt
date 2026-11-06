THREATLVCK REDESIGN - SETUP

1. BACK UP your current project folder first.
2. Keep your existing analyzer.py unchanged. It contains your original URL checks and risk scoring.
3. Replace app.py with the app.py in this package.
4. Replace templates/index.html and add:
   - templates/base.html
   - templates/login.html
   - templates/analytics.html
   - templates/settings.html
5. Replace static/css/style.css.
6. Add these JavaScript files:
   - static/js/dashboard.js
   - static/js/analytics.js
   - static/js/settings.js
   - static/js/earth.js
7. Keep your existing analyzer.py in the same folder as app.py.

PROJECT STRUCTURE
ThreatLvck/
  app.py
  analyzer.py                 (KEEP YOUR EXISTING FILE)
  templates/
    base.html
    login.html
    index.html
    analytics.html
    settings.html
  static/
    css/style.css
    js/dashboard.js
    js/analytics.js
    js/settings.js
    js/earth.js
  threatlvck.db               (created automatically on first run)

RUN
Install Flask and requests if not already installed:
  pip install flask requests

Run:
  python app.py

Open:
  http://127.0.0.1:5000

LOCAL DEMO LOGIN
  Username: admin
  Password: ThreatLvck@123

IMPORTANT SECURITY NOTE
The included login is a local classroom/demo login. Set these environment variables
before using beyond a local demo:
  THREATLVCK_SECRET = a long random secret
  THREATLVCK_USERNAME = your chosen username
  THREATLVCK_PASSWORD = a strong password

Analytics are stored in a local SQLite database (threatlvck.db). Only scans performed
after installing this version will appear. No historical scans are fabricated.
The scanner risk formula remains in your existing analyzer.py and is not changed.
