from twilio import twiml
from django_twilio.decorators import twilio_view
# include decompose in your views.py
from django_twilio.request import decompose
from django_twilio.client import twilio_client
from weddingsnap.models import Guest, Message, MessageImage

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.http import QueryDict
from django.core.urlresolvers import reverse

import os

@twilio_view
def broadcast_message(request):
    app_phone_number = os.environ.get('APP_PHONE_NUMBER')
    message = request.GET.get('message')
    if message is None:
        return HttpResponseBadRequest("No Message Sent.")
    guests = Guest.objects.filter(messaging_enabled=True)
    for guest in guests:
        twilio_client.messages.create(
        body=message,
        from_=app_phone_number,
        to=guest.phone_number,
        )
    return HttpResponse("Messages sent.")

@twilio_view
def text_message(request):

    response = twiml.Response()

    # Create a new TwilioRequest object
    twilio_request = decompose(request)

    # See the Twilio attributes on the class
    sender_phone_number = twilio_request.from_
    sent_message_sid = twilio_request.messagesid

    #if this is from me then redirect to broadcast
    my_phone_number = os.environ.get('MY_PHONE_NUMBER')
    if sender_phone_number == my_phone_number:
        qdict = QueryDict('',mutable=True)
        qdict.update({'message': twilio_request.body})
        redirect_url = reverse('broadcast_message')
        full_url = "%s?%s" % (redirect_url, qdict.urlencode())
        return HttpResponseRedirect( full_url )

    #get guest who sent this message
    guest,guest_created = Guest.objects.get_or_create(phone_number=sender_phone_number)

    #create message
    message,message_created = Message.objects.get_or_create(message_sid=sent_message_sid, guest=guest)
    message.text = twilio_request.body

    #get photos from message
    if int(twilio_request.nummedia) > 0 :
        #if this is the user's first photo, send a reply that we got it
        if guest.images.count() == 0:
            response.message("Thanks for sending us an image! This is a confirmation that we got it. We'll only send this once.")
        #do stuff
        for i in range(int(twilio_request.nummedia)):
            key = "{0}{1}".format("mediaurl",i)
            media_url = getattr(twilio_request, key)
            message_image,message_image_created = MessageImage.objects.get_or_create(
                url=media_url,
                message=message,
                guest=guest)
            message_image.save()

    guest.save()
    message.save()

    #if this is an unsubscribe, do it
    if message.text.lower() == "stop":
        guest.messaging_enabled = False
        guest.save()
        response.message("You've been unsubscribed from wedding updates!")
        return response

    return response
