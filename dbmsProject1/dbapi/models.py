from __future__ import unicode_literals

from django.db import models

class viewer(models.Model):
    name = models.CharField(max_length=200)
    id = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    follows = models.PositiveIntegerField()
    followers = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id) + ": " + self.name + "| follows:"+ str(self.follows) + "| followers"+ str(self.followers)

class genre(models.Model):
    genreId = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=200)
    popularity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.genreId) +" : "+ str(self.name)

class advertiser(models.Model):
    advertiserId = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    showTime = models.PositiveIntegerField(null=False)
    genreId = models.ForeignKey(genre, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.advertiserId) + ": " +self.name +" " + self.genreId.name

class channel(models.Model):
    channelId = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=200)
    ownerId = models.ForeignKey(viewer, on_delete=models.CASCADE)
    cost_multiplier = models.PositiveIntegerField()
    advertiserId = models.ForeignKey(advertiser)
    creationDate = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.channelId) + " : " + self.name + " : Owner : " + self.ownerId.name

class video(models.Model):
    videoId = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    views = models.PositiveIntegerField()
    channelId = models.ForeignKey(channel, on_delete=models.CASCADE)
    genreId = models.ForeignKey(genre)

    def __str__(self):
        return str(self.videoId) + " : " + self.title + " : channel : " + self.channelId.name

class subscription(models.Model):
    subscriptionId = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    channelId = models.ForeignKey(channel, on_delete=models.CASCADE)
    userId = models.ForeignKey(viewer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.userId.id) +" : " +self.userId.name+ " --> " +str(self.channelId.channelId) +" : " + self.channelId.name
