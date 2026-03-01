#!/usr/bin/env bash
pip install -r requirements.txt
cd workflow
python manage.py collectstatic --no-input
python manage.py migrate
```

**`Procfile`** (in root):
```
web: gunicorn workflow.wsgi:application --chdir workflow