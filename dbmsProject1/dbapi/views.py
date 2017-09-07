from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import *


# Create your views here.

global curUser


def login(request):
    html = loader.get_template('dbapi/index.html')
    context = {}
    return HttpResponse(html.render(context, request))


def home(request):
    username = request.GET['username']
    loggedUser = viewer.objects.filter(name=username)

    if loggedUser:
        global curUser
        curUser = loggedUser[0]
        html = loader.get_template('dbapi/home.html')
        all_videos = video.objects.all()
        context = {'all_videos': all_videos, 'user' : curUser}
    else:
        html = loader.get_template('dbapi/invalid_login.html')
        context = {}
    return HttpResponse(html.render(context, request))


def rethome(request):
    user = curUser

    if curUser:
        html = loader.get_template('dbapi/home.html')
        all_videos = video.objects.all()
        context = {'all_videos': all_videos, 'user' : curUser}
    else:
        html = loader.get_template('dbapi/invalid_login.html')
        context = {}
    return HttpResponse(html.render(context, request))


def subspage(request):

    user = curUser

    if user:
        html = loader.get_template('dbapi/subscription.html')
        subs = subscription.objects.filter(userId = user)
        channels = []
        for sub in subs:
            channels.append(sub.channelId)
        subbed_video = []
        for chan in channels:
            vid = video.objects.filter(channelId = chan.channelId)
            for v in vid:
                subbed_video.append(v)
        context = {'user' : user, 'all_videos': subbed_video}
    else:
        html = loader.get_template("dbapi/index.html")
        context = {}

    return HttpResponse(html.render(context, request))