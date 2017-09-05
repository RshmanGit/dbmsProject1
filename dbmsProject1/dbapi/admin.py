from django.contrib import admin
from .models import viewer, channel, advertiser, video, genre, subscription

admin.site.register(viewer)
admin.site.register(channel)
admin.site.register(advertiser)
admin.site.register(video)
admin.site.register(genre)
admin.site.register(subscription)