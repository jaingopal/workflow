#!/usr/bin/env bash
pip install -r requirements.txt
cd workflow
python manage.py collectstatic --no-input
python manage.py migrate