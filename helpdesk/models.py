from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token

STATUS_CHOICE = (('low', 'low'),
                 ('middle', 'middle'),
                 ('high', 'high'))


class Requisitions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICE, max_length=6, default='low')
    title = models.CharField(max_length=50)
    text = models.TextField()
    active_status = models.BooleanField(default=True)
    review = models.BooleanField(null=True, blank=True)
    recovery = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.status} ✔ {self.user} ✔ {self.title} ✔ {self.text} 	|Active:{self.active_status} |Accepted:{self.review}'


class Comment(models.Model):
    requisitions = models.ForeignKey(Requisitions, on_delete=models.CASCADE, related_name='comment_requisitions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    text = models.TextField()

    def __str__(self):
        return f'{self.user} : {self.text}'


class NewToken(Token):
    time_to_die = models.DateTimeField(default=timezone.now)
