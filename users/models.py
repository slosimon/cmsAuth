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
from __future__ import unicode_literals
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.utils import IntegrityError
from django.db import models
class UsersManager(models.Manager):
    def create_user(self, fn, ln, un, pas, email, time, lang):
        user = self.create(first_name=fn, last_name=ln, username=un, password=pas, email=email, timezone=time, preferred_languages=lang)
        # do something with the book
        return user


class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(unique=True, max_length=25)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    timezone = models.CharField(max_length=255, blank=True, null=True)
    preferred_languages = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = UsersManager()
    def __unicode__(self):
        return unicode(self.id)
#    @classmethod
#    def create_user(cls, username):
#        user = cls(username=username)
        # do something with the book
#        return user
    class Meta:
        managed = True
        db_table = 'users'

class Profile(models.Model):
    user = models.OneToOneField(Users, related_name='CMS_username') #1 to 1 link with Django User
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
class PassChange(models.Model):
    user = models.OneToOneField(Users, related_name='CMS_user')
    activation_key = models.CharField(max_length=40)

class Contests(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    allowed_localizations = models.CharField(max_length=255)
    languages = models.CharField(max_length=255)
    submissions_download_allowed = models.BooleanField()
    allow_questions = models.BooleanField()
    allow_user_tests = models.BooleanField()
    block_hidden_participations = models.BooleanField()
    allow_password_authentication = models.BooleanField()
    ip_restriction = models.BooleanField()
    ip_autologin = models.BooleanField()
    token_mode = models.TextField()  # This field type is a guess.
    token_max_number = models.IntegerField(blank=True, null=True)
    token_min_interval = models.TextField()  # This field type is a guess.
    token_gen_initial = models.IntegerField()
    token_gen_number = models.IntegerField()
    token_gen_interval = models.TextField()  # This field type is a guess.
    token_gen_max = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField()
    stop = models.DateTimeField()
    timezone = models.CharField(max_length=255, blank=True, null=True)
    per_user_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    max_submission_number = models.IntegerField(blank=True, null=True)
    max_user_test_number = models.IntegerField(blank=True, null=True)
    min_submission_interval = models.TextField(blank=True, null=True)  # This field type is a guess.
    min_user_test_interval = models.TextField(blank=True, null=True)  # This field type is a guess.
    score_precision = models.IntegerField()
    class Meta:
        managed = True
#        ordering=('name',)
        db_table = 'contests'


class Participations(models.Model):
    ip = models.CharField(max_length=255, blank=True, null=True)
    starting_time = models.DateTimeField(blank=True, null=True)
    delay_time = models.TextField()  # This field type is a guess.
    extra_time = models.TextField()  # This field type is a guess.
    password = models.CharField(max_length=255, blank=True, null=True)
    hidden = models.BooleanField()
    unrestricted = models.BooleanField()
    contest = models.ForeignKey(Contests, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, default="ZOTKS") # models.CharField(max_length=255,default=contest)
    def __unicode__(self):
        return unicode("ZOTKS")
    class Meta:
        managed = True
        ordering=('name',)
        db_table = 'participations'
class Teams(models.Model):
    code = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'teams'



