from django.contrib import admin
from watchlist.models import WatchList,StreamPlatform,Review
# Register your models here.
class WatchListAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(WatchList,WatchListAdmin)
admin.site.register(StreamPlatform)
admin.site.register(Review)
