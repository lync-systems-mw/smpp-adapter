# SMS Adapter

A web adapter that provides sms sending and reception functions for any application that deals with SMSs

## Installation

### Clone repository

```
git clone https://github.com/chiweto.ch/sms-transciever.git
```

### Create virtual env

To properly manage your instance and avoid dependency conflicts create a virtual environment using

```
pip install -m virtualenv
```

Then create your virtual environment with

<small>Preferably create it in the same dir as your project. We ignore this in our ignore</small>

```
virtualenv [venv or name of your environeent]
```

Activate your environment by running

```
source venv/bin/activate
```

<small>If you did not use venv , use the name of your environment</small>

### Install dependencies

Change into project directory and install python dependencies

```
pip install -r requirements.txt
```

### Run Migration

Create the database by runnning

```
python manage.py migrate
```

### Seeding Users

The smpptransfer app has a seedusers command that creates 2 default users:
(username and password)

1. chiweto -> @Adapter-2022!
2. olamula -> @Olamula-2022!

To create the default users run:

```bash
python manage.py seedusers
```

### Serving the application

Finally, serve the application by running

```
python manage.py runserver
```

## SMPP

### Getting Messages

Messages can be retrieved from the SMSC in 2 ways :

- Listening: actively listening for new incoming messages
- Pulling : once off poll that pull any pending messages from the SMSC

#### Listening

This requires running a daemon.

To start listening for messages from SMSC run the following command

```bash
python manage.py listen&
```

#### Pulling

To pull messages one time, useful in case the listener failed at some point, run

```bash
python manage.py pull
```

NB: You can also run a celery worker to automatically run the celery job scheduled at every 30 minutes.
Check out the section on running the celery worker.

### Sending Messages

Similar to getting messages, there are 2 way of sending message:

- Active Sending - sends out messages as they come into the adapter
- Pushing - once off push that sends outstanding unsent messages

#### Active Sending

This requires a daemon.

SMS sending using this methods is done via a background job, to process these background
job, run the following command

```bash
python manage.py process_tasks&
```

#### Pushing

To push retry sending unsent messages you can run the following command:

```bash
python manage.py push
```

Only messages that have not exceeded the maximum attempts threshold are retried.

The default is 4, but You can adjust this value in the settings files.

NB: You can also run a celery worker to automatically run a celery task scheduled at every hour.
Check out the section on running the celery worker.

## Celery Workers

The app has scheduled tasks that can automate certain processes such as resending unsent messages and
pulling pending messages to and from the SMSC.

To use this, we've configured the app to use REDIS as the broker
so you must have this setup on the machine and if using a remote REDIS server,
update the CELERY configuration in settings.

If all is setup, start your worker with Celery Beat using the following command:

```
celery -A smstransciever worker -B -l INFO
```

NB: The beat is what pushes periodic tasks to the worker and without it, the worker on processes
background jobs sent to it from the app. So it is important to start thr worker with the beat.

Alternatively if you want to run the worker and the beat as 2 seperate processes (for monitoring purposes)
you can run the following commands:

```bash
celery -A smstransciever worker -l INFO
```

```bash
celery -A smstransciever beat -l INFO
```