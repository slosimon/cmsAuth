"""cmsAuth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
"""

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

#from django.conf.urls.defaults import *
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from users import views as user_views
from django.utils.translation import ugettext as _
urlpatterns =[ 

    url(r'^$', user_views.register, name='registracija'),
#url(r'^register/(?P<user_id>\d+)/$', user_views.register, name='edit'),
url(r'^'+settings.ACTIVATE+r'/(?P<key>.+)$', user_views.activation, name='aktiviraj'),
url(r'^'+settings.NEW_LINK+r'/(?P<user_id>\d+)/$', user_views.new_activation_link, name='nova-povezava'),
url(r'^'+settings.THANKS+r'/(?P<user_id>\d+)/$', user_views.thanks, name='hvala'),
url(r'^'+settings.RECIEVED+r'/$', user_views.sprejeto, name='sprejeto'),
url(r'^'+settings.SUCCESS+r'/$', user_views.uspeh, name='uspeh'),
url(r'^'+settings.LOST_PASSWORD+r'/$', user_views.request_new_pass, name='pozabljeno-geslo'),
url(r'^'+settings.NEW_PASSWORD+r'/(?P<key>.+)$', user_views.new_pass, name='novo-geslo'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
