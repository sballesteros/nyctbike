from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

from models import Station, Idea, DesignStation, DesignBike, VoteIdea, VoteStation, VoteDesignStation, VoteDesignBike, News, UserProfile, SupportStation, SupportIdea, SupportDesignStation, SupportDesignBike

from forms import DesignForm, StationForm, ProfileForm, SupportForm, IdeaForm

from django.contrib.auth.models import User

import json
#from modl import ModelC
#from simforence.settings import PATH_TO_MODELC

import datetime

#the opposite of play isn't work -it's depression

def register(request):
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/')
        else:
            return render_to_response('registration/register.html',
                                      {'form':form,
                                       'current_menu':''},
                                      context_instance=RequestContext(request))
    else:
        form = UserCreationForm()

        return render_to_response('registration/register.html',
                                  {'form':form,
                                   'current_menu':''},
                                  context_instance=RequestContext(request))



def welcome(request):

    myStation = Station.objects.all()[0:1]
    #myIdea = Idea.objects.all()[0:1]
    #myDesignStation = DesignStation.objects.all()[0:1]
    #myDesignBike = DesignBike.objects.all()[0:1]
    #mySupport = Support.objects.all()[0:1]
    myNews = News.objects.all()

    return render_to_response('welcome.html',
                              {'station_list':myStation,
                               #'idea_list':myIdea,
                               #'design_station_list':myDesignStation,
                               #'design_bike_list':myDesignBike,
                               #'support_list':mySupport,
                               'news':myNews,
                               'display_station':True,
                               'display_content':False,
                               'display_comments':False,
                               'display_link':True,
                               'current_menu':'home'},
                              context_instance=RequestContext(request))

def isProfilUncomplete(request):

    isitUncomplete = False

    ## To submit an idea the profile has to be completed (Licensing...)
    data={'first_name':request.user.first_name,
          'last_name':request.user.last_name,
          'email':request.user.email}

    try:
        user_profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        isitUncomplete = True
    else:
        data2={
            'country':user_profile.country,
            'about':user_profile.about
            }
        data.update(data2) ##merge dict

        if any(map(lambda x: x=='', data.values())):
            isitUncomplete = True

    return isitUncomplete


@login_required
def profile(request, needAll=False):

    needAll=isProfilUncomplete(request)

    ##we display the form with the current data saved on our database so that the user can change or modify
    data={'first_name':request.user.first_name,
          'last_name':request.user.last_name,
          'email':request.user.email}

    try:
        user_profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        ##initial choice is USA
        data['country']='USA'
    else:
        data2={
            'country':user_profile.country,
            'about':user_profile.about
            }
        data.update(data2) ##merge dict

    form = ProfileForm(data)


    return render_to_response('registration/profile.html',
                              {'form': form,
                               'need_all': needAll,
                               'current_menu':'home'},
                              context_instance=RequestContext(request))



@login_required
def form_profile_ajax(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            try:
                user_profile = request.user.get_profile()
            except UserProfile.DoesNotExist:
                ##create profile
                user_profile = UserProfile(user=request.user)
                
            ##update profile
            user_profile.country = cd['country']
            user_profile.about = cd['about']
            user_profile.save()
            
            ##update User
            User.objects.filter(username=request.user.username).update(first_name = cd['first_name'],
                                                                       last_name = cd['last_name'],
                                                                       email = cd['email'] )

            #a cool thing to return the html generated by rendering a template in Json:
            #html = render_to_string(template, {'review': review })

            ##can also use: if request.is_ajax() to be sure that javascript is allowed
            return HttpResponse(json.dumps({'form_ok':True,
                                            'form_uncomplete':any(map(lambda x: x=='', cd.values())),
                                            'html':ProfileForm(cd).as_table()}),
                                mimetype='application/json')

        else: #form not valid, we resubmit it with error msg so that the user correct it

            return HttpResponse(json.dumps({'form_ok':False,
                                            'form_uncomplete':False,
                                            'html':form.as_table()}),
                                mimetype='application/json')

    else: ##user is not authentified
        return HttpResponseRedirect('/profile')



def userInfo(request):

    if 'username' in request.GET and request.GET['username']:
        myusername = str(request.GET['username'])

        try:
            myuser = User.objects.get(username=myusername)
        except User.DoesNotExist:
            return HttpResponseRedirect('/')
        else:
            #my stations: processed by ajax

            #my ideas:
            myIdeas = myuser.bike_idea_related.filter(activated='A')
            myDesignStations = myuser.bike_designstation_related.filter(activated='A')
            myDesignBikes = myuser.bike_designbike_related.filter(activated='A')

            return render_to_response('user.html',
                                      {'myuser':myuser,
                                       'myIdeas':{'idea':myIdeas},
                                       'myDesignStations':{'designstation':myDesignStations},
                                       'myDesignBikes':{'designbike':myDesignBikes},
                                       'display_content':False,
                                       'display_comments':False,
                                       'display_link':True,
                                       'current_menu':'home'},
                                      context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect('/')





def supported(request):

    myStations=Station.objects.filter(nbsupports__gte=1)
    myIdeas = Idea.objects.filter(nbsupports__gte=1)
    myDesignStations = DesignStation.objects.filter(nbsupports__gte=1)
    myDesignBikes = DesignBike.objects.filter(nbsupports__gte=1)

    return render_to_response('supported.html',
                              {'myStations':{'station':myStations},
                               'myIdeas':{'idea':myIdeas},
                               'myDesignStations':{'designstation':myDesignStations},
                               'myDesignBikes':{'designbike':myDesignBikes},
                               'display_content':False,
                               'display_comments':False,
                               'display_link':True,
                               'current_menu':'supported'},
                              context_instance=RequestContext(request))


def ideas(request):

    myideas_B = Idea.objects.filter(category='B', activated='A')
    myideas_F = Idea.objects.filter(category='F', activated='A')
    myideas_W = Idea.objects.filter(category='W', activated='A')
    myideas_O = Idea.objects.filter(category='O', activated='A')

    return render_to_response('ideas.html',
                              {'idea_list_B':{'idea':myideas_B},
                               'idea_list_F':{'idea':myideas_F},
                               'idea_list_W':{'idea':myideas_W},
                               'idea_list_O':{'idea':myideas_O},
                               'display_content':False,
                               'display_comments':False,
                               'display_link':True,
                               'current_menu':'idea'},
                              context_instance=RequestContext(request))


###MAKE this generic and call it display
def display(request, what):
    """display an idea and all the associated comments"""

    if 'id' in request.GET and request.GET['id']:
        myid=request.GET['id']

        if what=='idea':
            myobject = Idea.objects.get(id=myid)
        elif what=='designbike':
            myobject = DesignBike.objects.get(id=myid)
        else:
            myobject = DesignStation.objects.get(id=myid)

        return render_to_response('idea.html',
                                  {'object_list':{what:[myobject]} ,
                                   'display_content':True,
                                   'display_comments':True,
                                   'myid':myid,
                                   'current_menu':what},
                                  context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect('/ideas')


def designList(request, dtype):

    if dtype == 'designstation':
        mydesigns = DesignStation.objects.filter(activated='A')
    else:
        mydesigns = DesignBike.objects.filter(activated='A')


    return render_to_response('designlist.html',
                              {'type':dtype,
                               'mydesigns':mydesigns,
                               'current_menu':dtype},
                              context_instance=RequestContext(request))




@login_required
def submit(request, redirect, stype):

    ## To submit an idea the profile has to be completed (Licensing...)
    if isProfilUncomplete(request):
        return profile(request, True)
    else:
        if request.method == 'POST':

            if stype == 'idea':
                form = IdeaForm(request.POST)
            else:
                form = DesignForm(request.POST, request.FILES)

            if form.is_valid():
                cd = form.cleaned_data

                if stype == 'idea':
                    myt = Idea(name = cd['name'],
                               description = cd['description'],
                               creator = request.user,
                               category = cd['category'],
                               like = 0,
                               dontlike= 0,
                               dontcare = 0,
                               nbsupports = 0,
                               activated = 'A')
                elif stype == 'designstation':
                    myt = DesignStation(name = cd['title'],
                               description = cd['description'],
                               creator = request.user,
                               pict = cd['image'],
                               like = 0,
                               dontlike= 0,
                               dontcare = 0,
                               nbsupports = 0,
                               activated = 'A')
                else:
                    myt = DesignBike(name = cd['title'],
                               description = cd['description'],
                               creator = request.user,
                               pict = cd['image'],
                               like = 0,
                               dontlike= 0,
                               dontcare = 0,
                               nbsupports = 0,
                               activated = 'A')

                    
                myt.save()

                return HttpResponseRedirect(redirect)
            else:
                return render_to_response('submit.html',
                                          {'me': request.user.username,
                                           'form': form, 
                                           'current_menu':stype},
                                          context_instance=RequestContext(request))
        else:

            if stype == 'idea':
                form = IdeaForm()
            else:
                form = DesignForm()

            return render_to_response('submit.html',
                                      {'me': request.user.username,
                                       'form': form,
                                       'current_menu':stype},
                                      context_instance=RequestContext(request))



def stations(request):

    return render_to_response('stations.html',
                              {'current_menu':'station'},
                                  context_instance=RequestContext(request))


def serve_stations_data(request, public, latest, onlysupported):

    if public: #all stations
        if latest:
            mystations= [ Station.objects.all()[0] ]
        else:
            if onlysupported:
                mystations=Station.objects.filter(nbsupports__gte=1)
            else:
                mystations=Station.objects.all()

    elif 'username' in request.GET and request.GET['username']:
        myusername = str(request.GET['username'])

        myuser = User.objects.get(username=myusername)
        mystations=myuser.bike_station_related.all()

        

    else: #this should never happen
        return HttpResponseRedirect('/')


    data=[]
    for i in range(len(mystations)):
        data.append({
                'lat':mystations[i].lat,
                'lng':mystations[i].lon,
                'title':str(mystations[i].id)
                })

    outputjson=json.dumps(data)

    return HttpResponse(outputjson,
                        mimetype='application/json')



def get_station_info(request):

    if 'id' in request.GET and request.GET['id']:
        myid = int(request.GET['id'])
    else:
        #return empty template
        return render_to_response('display_station.html',
                                  {'display_station':False,
                                   'display_comments':False},
                                  context_instance=RequestContext(request))

    try:
        myStation=Station.objects.get(id=myid)
    except Station.DoesNotExist:
        #return empty template
        return render_to_response('display_station.html',
                                  {'display_station':False,
                                   'display_comments':False},
                                  context_instance=RequestContext(request))

    else:
        return render_to_response('display_station.html',
                                  {'object':myStation,
                                   'display_station':True,
                                   'display_comments':True,
                                   'display_link':False,
                                   'myid':myid,
                                   'type':'station'},
                                  context_instance=RequestContext(request))





@login_required
def submitComment(request, what): ##what has to be the URL of the object type as it will be used to redirect user after the comment is posted.
    
    if 'id' in request.GET and request.GET['id']:
        myid = request.GET['id']        

        if what=='station':
            myobject = Station.objects.get(id=myid)
        elif what=='idea':
            myobject = Idea.objects.get(id=myid)
        elif what=='designstation':
            myobject = DesignStation.objects.get(id=myid)
        else:
            myobject = DesignBike.objects.get(id=myid)

        return render_to_response('submitcomment.html',
                                  {'me': request.user.username,
                                   'current_menu':'station',
                                   'what': what,
                                   'object': myobject,
                                   'myid': myid,
                                   'current_menu':what},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/'+what+'s')


#def get_support_detail(request):
#
#    if 'id' in request.GET and request.GET['id']:
#        myid = int(request.GET['id'])
#    else:
#        #return empty template
#        return HttpResponse('<p>error</p>')
#
#    try:
#        mysupport=Support.objects.get(id=myid)
#    except Support.DoesNotExist:
#        #return empty template
#        return HttpResponse('<p>error</p>')
#
#    else:
#        mysupports=request.user.support_set.all().order_by("-when")
#
#        return render_to_response('display_support.html',
#                                  {'support_list':mysupports,
#                                   'display_content':True},
#                                  context_instance=RequestContext(request))
#
#


##@csrf_exempt
def vote_ajax(request, voteModelNameForeignKey, voteModelName, voteWhichModelName, mynext ):
    """exemple: call with:
    {'voteModelNameForeignKey':'votestation',
    'voteModelName':'VoteStation',
    'voteWhichModelName':'Station'}"""
    
    if request.user.is_authenticated():

        if request.method == 'POST':
        #user can vote only once
        
            myid= request.POST[ 'idobject' ]
            
            try:
                previousvote = eval('request.user.bike_' + voteModelNameForeignKey + '_related.get(which__id = myid )') #note the use of __id to access id field of the ForeignKey

            except eval(voteModelName+'.DoesNotExist'):


                likeit = request.POST['vote']


                #vote
                mywhich = eval(voteWhichModelName+'.objects.get(id=myid)')
                myvote = eval(voteModelName+'(creator=request.user, which=mywhich, vote=likeit)')
                myvote.save()

                #count the vote
                if likeit == 'L':
                    mywhich.like += 1
                    count=mywhich.like
                elif likeit == 'C':
                    mywhich.dontcare += 1
                    count=mywhich.dontcare
                else:
                    mywhich.dontlike += 1
                    count=mywhich.dontlike


                mywhich.save()

                return HttpResponse(json.dumps({'already':0,
                                                'id':myid,
                                                'nb':count,
                                                'what': likeit,
                                                'auth':True}),
                                    mimetype='application/json')

            else:                
                prt='like'
                if previousvote.vote == 'L':
                    pass
                elif previousvote.vote == 'C':
                    prt="don't care"
                else:
                    prt="don't like"

                return HttpResponse(json.dumps({'already':1,
                                                'id':myid,
                                                'auth':True,
                                                'what': prt,
                                                'when': previousvote.when.isoformat()
                                                }),
                                    mimetype='application/json')
    else:
        return HttpResponse(json.dumps({'auth':False,
                                        'next':mynext}),
                            mimetype='application/json')


@login_required
def submitstation(request):

    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            mystation = Station(lat = cd['latitude'],
                                lon = cd['longitude'],
                                why = cd['why'],
                                comment = cd['comment'],
                                creator = request.user,
                                like = 0,
                                dontlike= 0,
                                dontcare = 0,
                                nbsupports = 0,
                                activated = 'A')

            mystation.save()

            mystations=Station.objects.all()[0:1]
            return HttpResponseRedirect('/stations?id={0}'.format(mystations[0].id))

    else:

        form = StationForm()

    return render_to_response('submitstation.html',
                                  {'current_menu':'station',
                                   'me': request.user.username,
                                   'form': form},
                                  context_instance=RequestContext(request))



@login_required
def support(request, what):

    if isProfilUncomplete(request):
        return profile(request, True)
    else:

        if request.method == 'POST':

            myid = request.POST['idobject']
            if what=='station':
                myobject = Station.objects.get(id=myid)
            elif what=='idea':
                myobject = Idea.objects.get(id=myid)
            elif what=='designstation':
                myobject = DesignStation.objects.get(id=myid)
            else:
                myobject = DesignBike.objects.get(id=myid)

            form = SupportForm(request.POST)

            if form.is_valid():
                cd = form.cleaned_data


                myobject.nbsupports +=1
                myobject.save()

                if what=='station':
                    mys = SupportStation(creator = request.user,
                                  description = cd['description'],
                                  supported = myobject,
                                  amount = cd['amount'])
                elif what=='idea':
                    mys = SupportIdea(creator = request.user,
                                  description = cd['description'],
                                  supported = myobject,
                                  amount = cd['amount'])
                elif what=='designstation':
                    mys = SupportDesignStation(creator = request.user,
                                  description = cd['description'],
                                  supported = myobject,
                                  amount = cd['amount'])
                else:
                    mys = SupportDesignBike(creator = request.user,
                                  description = cd['description'],
                                  supported = myobject,
                                  amount = cd['amount'])

                mys.save()

                return HttpResponseRedirect('/thanks')

            else:
                return render_to_response('support.html',
                                          {'me': request.user.username,
                                           'object':myobject,
                                           'form': form,
                                           'current_menu':what},
                                          context_instance=RequestContext(request))
        else:

            if 'idobject' in request.GET and request.GET['idobject']:
                myid = str(request.GET['idobject'])
                
                try:
                    if what=='station':
                        myobject = Station.objects.get(id=myid)
                    elif what=='idea':
                        myobject = Idea.objects.get(id=myid)
                    elif what=='designstation':
                        myobject = DesignStation.objects.get(id=myid)
                    else:
                        myobject = DesignBike.objects.get(id=myid)

                except: ## Idea.DoesNotExist:
                    return HttpResponseRedirect('/what'+'s')
                else:
                    form = SupportForm()

                    return render_to_response('support.html',
                                              {'me': request.user.username,
                                               'object':myobject,
                                               'form': form,
                                               'current_menu':what},
                                              context_instance=RequestContext(request))




