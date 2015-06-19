from django.db import models

class Guest(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=20)
    messaging_enabled = models.BooleanField(default=True)

    def __str__(self):
            return "%s %s %s" % (self.first_name,
            self.last_name,
            self.phone_number)

class Message(models.Model):
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    guest = models.ForeignKey(Guest, related_name="messages")
    message_sid = models.CharField(max_length=50)

    def __str__(self):
        return "%s from %s" % (self.text, self.guest.phone_number)

class MessageImage(models.Model):
    url = models.URLField()
    message = models.ForeignKey(Message, related_name="images")
    guest = models.ForeignKey(Guest, related_name="images")
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "MessageImage at %s" % self.url
