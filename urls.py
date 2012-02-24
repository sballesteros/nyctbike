from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login, logout

from nyctbike.bike import views


#For example:
#
#urlpatterns = patterns('blog.views',
#    (r'^blog/(?P<year>\d{4})/$', 'year_archive', {'foo': 'bar'}),
#)
#
#In this example, for a request to /blog/2005/, Django will call the blog.views.year_archive() view, passing it these keyword arguments:

urlpatterns = patterns('',
                       (r'^$', views.welcome),
                       (r'^comments/', include('django.contrib.comments.urls')),
                       
                       (r'^stations/$', views.stations),
                       (r'^get_station_info/$', views.get_station_info),
                       (r'^serve_stations_data_supported/$', views.serve_stations_data, {'public':True, 'latest':False, 'onlysupported':True}),
                       (r'^serve_stations_data/$', views.serve_stations_data, {'public':True, 'latest':False, 'onlysupported':False}),
                       (r'^serve_stations_data_latest/$', views.serve_stations_data, {'public':True, 'latest':True, 'onlysupported':False}),
                       (r'^serve_stations_data_user/$', views.serve_stations_data, {'public':False, 'latest':False, 'onlysupported':False}),
                       
                       (r'^vote_station_ajax/$', views.vote_ajax, {'voteModelNameForeignKey':'votestation',
                                                                   'voteModelName':'VoteStation',
                                                                   'voteWhichModelName':'Station',
                                                                   'mynext':'/stations/'} ),
                       (r'^vote_idea_ajax/$', views.vote_ajax, {'voteModelNameForeignKey':'voteidea',
                                                                'voteModelName':'VoteIdea',
                                                                'voteWhichModelName':'Idea',
                                                                'mynext':'/ideas/'} ),
                       (r'^vote_designstation_ajax/$', views.vote_ajax, {'voteModelNameForeignKey':'votedesignstation',
                                                                'voteModelName':'VoteDesignStation',
                                                                'voteWhichModelName':'DesignStation',
                                                                'mynext':'/designstations/'} ),
                       (r'^vote_designbike_ajax/$', views.vote_ajax, {'voteModelNameForeignKey':'votedesignbike',
                                                                'voteModelName':'VoteDesignBike',
                                                                'voteWhichModelName':'DesignBike',
                                                                'mynext':'/designbikes/'} ),


                       
                       (r'^about/', TemplateView.as_view(template_name="about.html")),
                       (r'^thanks/', TemplateView.as_view(template_name="thanks.html")),
                       (r'^license/', TemplateView.as_view(template_name="licence.html")),
                       (r'^donate/', TemplateView.as_view(template_name="donate.html")),
                       
                       #    (r'^get_involved/$', views.get_involved),
#    (r'^get_support_detail/$', views.get_support_detail),


                       (r'^supportstation/$', views.support, {'what':'station'}),
                       (r'^supportidea/$', views.support, {'what':'idea'}),
                       (r'^supportdesignbike/$', views.support, {'what':'designbike'}),
                       (r'^supportdesignstation/$', views.support, {'what':'designstation'}),                       

                       (r'^idea/$', views.display, {'what':'idea'}),
                       (r'^designbike/$', views.display, {'what':'designbike'}),
                       (r'^designstation/$', views.display, {'what':'designstation'}),

                       (r'^ideas/$', views.ideas),
                       (r'^designstations/$', views.designList, {'dtype':'designstation'}),
                       (r'^designbikes/$', views.designList, {'dtype':'designbike'}),
                       (r'^supported/$', views.supported),

                       (r'^submitidea/$', views.submit, {'redirect':'/ideas', 'stype':'idea'}),
                       (r'^submitdesignstation/$', views.submit, {'redirect':'/designstations', 'stype':'designstation'}),
                       (r'^submitdesignbike/$', views.submit, {'redirect':'/designbikes', 'stype':'designbike'}),
                       
                       
                       (r'^submitstation/$', views.submitstation),
                       (r'^submitcommentstation/$', views.submitComment,  {'what':'station'}),
                       (r'^submitcommentidea/$', views.submitComment,  {'what':'idea'}),
                       (r'^submitcommentdesignstation/$', views.submitComment,  {'what':'designstation'}),
                       (r'^submitcommentdesignbike/$', views.submitComment,  {'what':'designbike'}),

                       
                       (r'^registration/register/$', views.register),
                       (r'^accounts/login/$', login),
                       (r'^accounts/logout/$', logout, {'next_page': '/accounts/login/'}),
                       
                       (r'^profile/$', views.profile),
                       (r'^form_profile_ajax/$', views.form_profile_ajax),
                       
                       (r'^user/$', views.userInfo),
                       # Uncomment the admin/doc line below to enable admin documentation:
                           # (r'^admin/doc/', views.include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin:
                           (r'^admin/', include(admin.site.urls)),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^site_media/(?P<path>.*)$',
                             'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
                            )
    
