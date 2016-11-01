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

import datetime
from django.template import Context
from django.core.mail import EmailMessage
from django import forms
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.core.mail import send_mail
from users.models import Users, Profile, PassChange
from django.utils.translation import ugettext as _
from django.conf import settings
url= settings.URL
class RegistrationForm(forms.Form):
    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': _("Name"),'class':'form-control input-perso'}),max_length=30,min_length=3)
    last_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': _("Surname"),'class':'form-control input-perso'}),max_length=30,min_length=3)
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': _("Username"),'class':'form-control input-perso'}),max_length=30,min_length=3)
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder': _("Email"),'class':'form-control input-perso'}),max_length=100,error_messages={'invalid': (_("Invalid email"))})
    password1 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': _("Password (min 6 chars)"),'class':'form-control input-perso'}))
    password2 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': _("Confirm your password"),'class':'form-control input-perso'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = ErrorList([_(u"Passwords don't match.")])

        return self.cleaned_data
    def save(self, datas):
        u = Users.objects.create_user(datas['first_name'],
                                     datas['last_name'],
                                     datas['username'],
                                     datas['password'],
                                     datas['email'],
                                   datas['timezone'],
                                     datas['preferred_languages'])
        u.is_active = False
        u.save()
        profile=Profile()
        profile.user=u
        profile.activation_key=datas['activation_key']
        profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()
        return u

    def sendEmail(self, datas):
        link=url+settings.ACTIVATE+"/"+datas['activation_key']
        c=Context({'activation_link':link,'username':datas['username']})
        t = get_template('email.txt') #make email.txt in templates
        message=t.render(c)
        email = EmailMessage(_("CMS Registration"), message, to=[datas['email']])
        email.send()
class EmailForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(EmailForm,self).__init__(*args,**kwargs)
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder': _("Email"),'class':'form-control input-perso'}),max_length=100,error_messages={'invalid': (_("Invalid email."))})
    def save(self, datas):
        u=Users.objects.get(id=self.user_id)
        a=u.is_active
        if not a:
            u.email=datas['email']
            u.save()
            Profile.objects.filter(user_id=self.user_id).delete()
            profile=Profile()
            profile.user=u
            profile.activation_key=datas['activation_key']
            profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
            profile.save()
        return u

    def sendEmail(self, datas):
        link=url+settings.ACTIVATE+"/"+datas['activation_key']
        c=Context({'activation_link':link, 'username':datas['username']})
        t = get_template('email.txt')
        message=t.render(c)
        email = EmailMessage(_("CMS registration"), message, to=[datas['email']])
        email.send()

class Email2Form(forms.Form):
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder': _("Email"),'class':'form-control input-perso'}),max_length=100,error_messages={'invalid': (_("Invalid email."))})
    def save(self, datas):
        u=Users.objects.get(email=datas['email'])
        pas = PassChange()
        pas.user=u
        pas.activation_key = datas['activation_key']
        pas.save()
    def sendEmail(self, datas):
        link=url+settings.NEW_PASSWORD+"/"+datas['activation_key']
        c=Context({'activation_link':link, 'username':datas['username']})
        t = get_template('email-pass.txt')
        message=t.render(c)
        email = EmailMessage(_("CMS lost password"), message, to=[datas['email']])
        email.send()


class PasswordForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(PasswordForm,self).__init__(*args,**kwargs)
    password1 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': _("Password (min 6 characters)"),'class':'form-control input-perso'}))
    password2 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': _("Confirm password"),'class':'form-control input-perso'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = ErrorList([_(u"Passwords don't match")])

        return self.cleaned_data
    def save(self, datas):
        u=Users.objects.get(id=self.user_id)
        a=u.is_active
        u.password=datas['password']
        u.save()
        Profile.objects.filter(user_id=self.user_id).delete()
        profile=Profile()
        profile.user=u
        profile.activation_key=datas['activation_key']
        profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()
        return u

    def sendEmail(self, datas):
        link=url+settings.ACTIVATE+"/"+datas['activation_key']
        c=Context({'activation_link':link,'username':datas['username']})
        t = get_template('email-pass.txt')
        message=t.render(c)
        email = EmailMessage(_("CMS password"), message, to=[datas['email']])
        email.send()
     
