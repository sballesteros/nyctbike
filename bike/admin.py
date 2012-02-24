from django.contrib import admin
from models import Station, Idea, DesignStation, DesignBike, VoteIdea, VoteStation, VoteDesignStation, VoteDesignBike, Support, News, UserProfile

class StationAdmin(admin.ModelAdmin):
    list_display= ('creator', 'activated', 'when')
    list_filter = ('when',)
    search_fields = ('creator',)

class IdeaAdmin(admin.ModelAdmin):
    list_display= ('creator', 'name', 'when')
    list_filter = ('when',)
    search_fields = ('name',)

admin.site.register(Station, StationAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(News)
admin.site.register(DesignStation)
admin.site.register(DesignBike)





