# Django CronJob

dead simple crontab powered job scheduling for django
for more informations, please check : https://pypi.org/project/django-crontab/
## setup

install via pip:.
```
pip install django-crontab
```

add it to installed apps in django settings.py:.
```
INSTALLED_APPS = (
    'django_crontab',
    
)
```

now create a new method that should be executed by cron every 5 minutes, f.e. in transcribe-frontend/workers.process.py:.
```
def my_scheduled_job():
  pass
```

now add this to your settings.py:.
```
CRONJOBS = [
    ('*/5 * * * *', 'myapp.cron.my_scheduled_job')
]
```

you can also define positional and keyword arguments which let you call django management commands:.
```
CRONJOBS = [
    ('*/5 * * * *', 'myapp.cron.other_scheduled_job', ['arg1', 'arg2'], {'verbose': 0}),
    ('0   4 * * *', 'django.core.management.call_command', ['clearsessions']),
]
```

finally run this command to add all defined jobs from CRONJOBS to crontab (of the user which you are running this command with:.
```
python manage.py crontab add
```

show current active jobs of this project:.
```
python manage.py crontab show
```

removing all defined jobs is straight forward:.
```
python manage.py crontab remove
```