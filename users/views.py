# -*- coding: utf-8 -*-
# cmsAuth - http://github.com/slosimon/cmsAuth/
# Copyright © 2016 Simon Weiss <weiss.simon.1995@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.from django.shortcuts

import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from users.forms import RegistrationForm, EmailForm, PasswordForm, Email2Form
from django.template import Context, RequestContext
import hashlib
import random
from users.models import Users, Profile, Participations, PassChange
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.conf import settings
#url="http://212.235.186.231/uporabnik/" #Default link to Django user app
#cmsUrl="http://212.235.186.231/"
# Create your views here.
lpl=settings.LOST_PASSWORD
def sprejeto(request):
    return render(request, 'sprejeto.html',{'u':settings.CMS_URL, 'lpl':lpl},locals())
def uspeh(request):
    return render(request, 'uspeh.html', {'u':settings.CMS_URL, 'lpl':lpl},locals())
def register(request):
    registration_form = RegistrationForm()
    context=RequestContext(request)
    l=[]
    if request.method == 'POST':
       form = RegistrationForm(request.POST)
       if form.is_valid():
            datas={}
            datas['first_name']=form.cleaned_data['first_name']
            datas['last_name']=form.cleaned_data['last_name']
            datas['username']=form.cleaned_data['username']
            datas['password']=form.cleaned_data['password1']
            datas['email']=form.cleaned_data['email']
            datas['timezone']=settings.TIME_ZONE
            datas['preferred_languages']="[\""+settings.LANGUAGE_CODE+"\"]" 
            #We generate a random activation key
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            usernamesalt = datas['username']
            if isinstance(usernamesalt, unicode):
                usernamesalt = usernamesalt.encode('utf8')
            datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

            datas['email_path']="/ActivationEmail.txt"
            datas['email_subject']=_("Activate your account for CMS")

            form.sendEmail(datas)
            form.save(datas) #Save the user and his profile
            el=get_object_or_404(Users, username = datas['username'])
            request.session['registered']=True #For display purposes
            return redirect(settings.URL+settings.THANKS+"/"+str(el.id)+"/") #
       else:
            registration_form = form #Display form with error messages (incorrect fields, etc)
    return render(request, 'register.html', {'formset':registration_form, 'u':settings.CMS_URL, 'lpl':lpl}, locals())

def activation(request, key):
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if profile.user.is_active == False:
        if timezone.now() > profile.key_expires:
            activation_expired = True #Display: offer the user to send a new activation link
            id_user = profile.user.id
        else: #Activation successful
            profile.user.is_active = True
            profile.user.save()
            c=Participations()
            c.delay_time="00:00:00" 
            c.extra_time="00:00:00"
            c.hidden="f"
            c.unrestricted="f"
            c.contest_id=settings.CONTEST_ID 
            c.user_id=profile.user.id
            c.name="ZOTKS" #change this too if you want. 
            c.save()
    else:
        already_active = True #Display : error message
    return render(request, 'aut.html',{'u':settings.CMS_URL, 'lpl':lpl}, locals())

def new_activation_link(request, user_id):
    form = RegistrationForm()
    datas={}
    user = Users.objects.get(id=user_id)
    if user is not None and not user.is_active:
        datas['first_name']=user.first_name
        datas['last_name']=user.last_name
        datas['username']=user.username
        datas['email_path']="/ResendEmail.txt"
        datas['email_subject']=_("New activation key for CMS")

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = datas['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

        profile = Profile.objects.get(user=user)
        profile.activation_key = datas['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()

        form.sendEmail(datas)
        request.session['new_link']=True #Display: new link sent
        return render(request,'register.html',{'u':settings.CMS_URL, 'lpl':lpl},locals())
    else:
        return redirect(settings.CMS_URL)

def request_new_pass(request):
    registration_form = Email2Form()
    context=RequestContext(request)
    l=[]
    if request.method == 'POST':
       form = Email2Form(request.POST)
       if form.is_valid():
            datas={}
            datas['email']=form.cleaned_data['email']
            user = Users.objects.get(email=datas['email'])
            datas['username']=user.username
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            el=get_object_or_404(Users, email = datas['email'])
            usernamesalt = el.username
            if isinstance(usernamesalt, unicode):
                usernamesalt = usernamesalt.encode('utf8')
            datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

            datas['email_path']="/ActivationEmail.txt"
            datas['email_subject']=_("Change your CMS password")

            form.sendEmail(datas)
            form.save(datas) #Save the user and his profile
            request.session['registered']=True #For display purposes
            return redirect(settings.URL+settings.RECIEVED+"/") #
       else:
            registration_form = form #Display form with error messages (incorrect fields, etc)
    return render(request, 'req-np.html', {'formset':registration_form, 'u':settings.CMS_URL, 'lpl':lpl}, locals())



def new_pass(request, key):
    pas = get_object_or_404(PassChange, activation_key = key)
    user = get_object_or_404(Users, id=pas.user_id)
    registration_form = PasswordForm(user_id=user.id)
    context=RequestContext(request)
    l=[]
    if request.method == 'POST':
       form = PasswordForm(request.POST, user_id=user.id)
       if form.is_valid():
            datas={}
            datas['first_name']=user.first_name
            datas['last_name']=user.last_name
            datas['username']=user.username
            datas['password']=form.cleaned_data['password1']
            datas['email']=user.email
            datas['timezone']=settings.TIME_ZONE 
            datas['preferred_languages']="[\""+settings.LANGUAGE_CODE+"\"]" 
            datas['activation_key']=pas.activation_key
            form.save(datas) #Save the user and his profile
            el=get_object_or_404(Users, username =user.username)
            request.session['registered']=True #For display purposes
            PassChange.objects.filter(activation_key=key).delete()
            return redirect(settings.URL+settings.SUCCESS+"/")
       else:
            registration_form = form #Display form with error messages (incorrect fields, etc)
    return render(request, 'set_pass.html', {'user':user, 'formset':registration_form, 'u':settings.CMS_URL, 'lpl':lpl}, locals())

def thanks(request, user_id):
    user = get_object_or_404(Users, id = user_id)
    registration_form = EmailForm(user_id=user_id)
    context=RequestContext(request)
    l=[]
    if request.method == 'POST':
       form = EmailForm(request.POST, user_id=user_id)
       if form.is_valid():
            datas={}
            datas['first_name']=user.first_name
            datas['last_name']=user.last_name
            datas['username']=user.username
            datas['password']=user.password
            datas['email']=form.cleaned_data['email']
            datas['timezone']=settings.TIME_ZONE
            datas['preferred_languages']="[\""+settings.LANGUAGE_CODE+"\"]"
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            usernamesalt = datas['username']
            if isinstance(usernamesalt, unicode):
                usernamesalt = usernamesalt.encode('utf8')
            datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

            datas['email_path']="/ActivationEmail.txt"
            datas['email_subject']=_("Activate your user account for CMS")
            if not user.is_active:
                form.sendEmail(datas)
                form.save(datas) #Save the user and his profile
            el=get_object_or_404(Users, username =user.username)
            request.session['registered']=True #For display purposes
            return redirect(settings.URL+settings.THANKS+"/"+str(user.id)+"/") 
       else:
            registration_form = form #Display form with error messages (incorrect fields, etc)



    return render(request, 'thanks.html', {'user':user, 'formset':registration_form, 'u':settings.CMS_URL, 'lpl':lpl}, locals())
