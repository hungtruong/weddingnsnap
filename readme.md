Weddingsnap
======
I got married and wanted to set up a way for our guests to share their photos of the special day with us. This is a Twilio app written with the [Django](https://www.djangoproject.com/) web framework and the [django-twilio](https://github.com/rdegges/django-twilio) framework which also uses [twilio-python](https://github.com/twilio/twilio-python). You can read more about the project on [my blog](http://www.hung-truong.com/blog/2015/06/18/collecting-wedding-photos-with-twilio-mms/).

## Features
1. Broadcast messages to guests throughout the day.
2. Accept messages that contain MMS images (one or more) and save their urls to a database.
3. Allow guests to "unsubscribe" to messages in case they didn't want them.

## Installation
To get this thing up and running, you'll need to set a few environmental variables:

* TWILIO_ACCOUNT_SID (your Twilio account SID)
* TWILIO_AUTH_TOKEN (your Twilio account token)
* DJANGO_SECRET_KEY (a secret key for Django)
* DATABASE_URL (you can use a sqlite url for this for local development)
* APP_PHONE_NUMBER (phone number that the Twilio app will use)
* MY_PHONE_NUMBER (phone number you can use to broadcast messages to all your guests)

The variables will need to be set for your virtualenv (in development) and Heroku (I'm assuming you're using Heroku for production). The DATABASE_URL variable is only required for development as Heroku provides that if you add postgresql to your app.

## Note
This app wasn't meant for any hardcore usage, just a hack for a day, so if it doesn't work, you could let me know in a Github issue. I just quickly gutted the app I had running of any hardcoded things like my phone number so I could throw this on Github.


## Copyright
I'm pretty sure there's already some product named "weddingsnap" but this was my internal name for it while developing it, so whatever. The source code is licensed under the MIT license; you can find it in this repo.
