# -*- encoding: utf-8 -*-
from django.db import models

class Tweet(models.Model):
    twitter_id = models.BigIntegerField()
    text = models.CharField(max_length=255)
    date = models.DateTimeField()

class Data(models.Model):
    access_token = models.CharField(max_length=255)
    access_token_secret = models.CharField(max_length=255)

