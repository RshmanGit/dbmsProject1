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
        context = {'all_videos': all_videos, 'user': curUser}
    else:
        html = loader.get_template('dbapi/invalid_login.html')
        context = {}
    return HttpResponse(html.render(context, request))


def rethome(request):

    user = curUser

    if user:
        html = loader.get_template('dbapi/home.html')
        all_videos = video.objects.all().order_by('-videoId')
        context = {'all_videos': all_videos, 'user': curUser}
    else:
        html = loader.get_template('dbapi/invalid_login.html')
        context = {}

    global curUser
    curUser = user
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
            vid = video.objects.filter(channelId = chan.channelId).order_by('-videoId')
            for v in vid:
                subbed_video.append(v)
        context = {'user': user, 'all_videos': subbed_video}
    else:
        html = loader.get_template("dbapi/index.html")
        context = {}

    global curUser
    curUser = user
    return HttpResponse(html.render(context, request))


def channelpage(request):

    user = curUser

    if user:
        html = loader.get_template("dbapi/mychannels.html")
        all_channels = []

        channels = channel.objects.filter(ownerId = user)
        for chan in channels:
            all_channels.append(chan)

        advertisers = advertiser.objects.all()

        all_genre = genre.objects.all()

        context = {'user': user, 'all_channels': all_channels, 'all_adverts': advertisers, "all_genre": all_genre}
    else:

        html = loader.get_template("dbapi/index.html")
        context = {}

    global curUser
    curUser = user
    return HttpResponse(html.render(context, request))


def createchannel(request):

    user = curUser

    if user:
        all_channels = []

        channels = channel.objects.filter(ownerId=user)
        for chan in channels:
            all_channels.append(chan)

        advertisers = advertiser.objects.all()

        all_genre = genre.objects.all()

        lastid = channel.objects.all().order_by('-channelId')[0].channelId
        newadvertiser = advertiser.objects.filter(name = request.GET['advertiser'])[0]
        newchannel = channel(channelId=lastid+1, name=request.GET['channelname'], ownerId = user, cost_multiplier = 10, \
                             advertiserId = newadvertiser, creationDate = '2015-07-07')
        newchannel.save()

        html = loader.get_template("dbapi/mychannels.html")
        context = {'user': user, 'all_channels': all_channels, 'all_adverts': advertisers, "all_genre": all_genre}

    else:
        html = loader.get_template("dbapi/index.html")
        context = {}

    global curUser
    curUser = user
    return HttpResponse(html.render(context, request))


def uploadvideo(request):
    user = curUser

    #videotitle=How+to+code&videodescription=Learn&channelid=ProgrammingKnowledge

    if user:
        all_channels = []

        channels = channel.objects.filter(ownerId=user)
        for chan in channels:
            all_channels.append(chan)

        advertisers = advertiser.objects.all()

        all_genre = genre.objects.all()

        lastid = video.objects.all().order_by('-videoId')[0].videoId

        newvideo = video(videoId = lastid+1, title = request.GET['videotitle'], description = request.GET['videodescription'], \
                         views = 0, channelId = channel.objects.filter(name = request.GET['channelid'])[0], \
                         genreId = genre.objects.filter(name = request.GET['genreid'])[0])

        newvideo.save()

        html = loader.get_template("dbapi/mychannels.html")
        context = {'user': user, 'all_channels': all_channels, 'all_adverts': advertisers, "all_genre": all_genre}

    else:
        html = loader.get_template("dbapi/index.html")
        context = {}

    global curUser
    curUser = user
    return HttpResponse(html.render(context, request))


def channeldesc(request, channelId):
    user = curUser

    pageschannel = channel.objects.filter(channelId = channelId)[0]

    if user:
        html = loader.get_template("dbapi/channel.html")

        all_videos = []
        all_videos = video.objects.filter(channelId = pageschannel.channelId)

        all_channels = []
        channels = channel.objects.filter(ownerId=user)
        for chan in channels:
            all_channels.append(chan)

        all_genre = genre.objects.all()

        subscribed = False
        subChannels = subscription.objects.filter(channelId = pageschannel)
        for sub in subChannels:
            if(sub.userId == user):
                subscribed = True

        context = {'user': user, 'channel': pageschannel, 'all_videos': all_videos,  'all_channels': all_channels, \
                   "all_genre": all_genre, 'subscribed': subscribed}

    else:
        html = loader.get_template("dbapi/index.html")
        context = {}

    return HttpResponse(html.render(context, request))


def subscribe(request, channelId):
    user = curUser

    pageschannel = channel.objects.filter(channelId=channelId)[0]

    if user:

        lastid = subscription.objects.all().order_by('-subscriptionId')[0].subscriptionId
        newsubscription = subscription(subscriptionId = lastid + 1, channelId = pageschannel, userId = user)
        newsubscription.save()

        html = loader.get_template("dbapi/channel.html")

        all_videos = []
        all_videos = video.objects.filter(channelId=pageschannel.channelId)

        all_channels = []
        channels = channel.objects.filter(ownerId=user)
        for chan in channels:
            all_channels.append(chan)

        all_genre = genre.objects.all()

        subscribed = False
        subChannels = subscription.objects.filter(channelId=pageschannel)
        for sub in subChannels:
            if (sub.userId == user):
                subscribed = True

        context = {'user': user, 'channel': pageschannel, 'all_videos': all_videos, 'all_channels': all_channels, \
                   "all_genre": all_genre, 'subscribed': subscribed}

    else:
        html = loader.get_template("dbapi/index.html")
        context = {}

    return HttpResponse(html.render(context, request))


def register(request):
    html = loader.get_template("dbapi/register.html")
    context = {}
    return HttpResponse(html.render(context, request))


def register_complete(request):
    newUsername = request.GET['username']
    lastid = viewer.objects.all().order_by('-id')[0].id

    newUser = viewer(name = newUsername, id = lastid + 1, follows = 0, followers = 0)
    newUser.save()

    print newUser

    html = loader.get_template("dbapi/index.html")
    context = {}
    return HttpResponse(html.render(context, request))


def videodesc(request, videoId):
    user = curUser
    pagesvideo = video.objects.filter(videoId=videoId)[0]
    pageschannel = channel.objects.filter(channelId=pagesvideo.channelId.channelId)[0]

    if user:
        html = loader.get_template("dbapi/video.html")
        subscribed = False
        subChannels = subscription.objects.filter(channelId=pageschannel)
        for sub in subChannels:
            if (sub.userId == user):
                subscribed = True
        context = {'video': pagesvideo, 'channel' : pageschannel, 'user': user, 'subscribed': subscribed}

    else:
        html = loader.get_template("dbapi/index.html")
        context = {}
    return HttpResponse(html.render(context, request))

